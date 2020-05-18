from django.shortcuts import render
from django.views import generic
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.db import IntegrityError
from .email_sender import send
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RegisterView(generic.View):
    template_name = 'authentication/registration.html'
    user_exists_template_name = 'authentication/user_exists.html'
    confirm_template_name = 'authentication/confirm.html'
    context_object_name = 'context'

    def get_context(self, **kwargs):
        context = {}
        context['register_form'] = RegisterForm()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = RegisterForm(self.request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['user_email']
            first_name = user_form.cleaned_data['first_name']
            second_name = user_form.cleaned_data['second_name']
            password = user_form.cleaned_data['password']

            try:
                user = _create_user(email, first_name, second_name, password)
                logger.info("Created user " + first_name)
            except IntegrityError:
                logger.warning("User already exists!")
                return render(request, self.user_exists_template_name, {})

            _send_activation_email(email, user, request)

            return render(request, self.confirm_template_name, {})
        else:
            logger.warning("User data is invalid")
            form = RegisterForm()
            return render(request, self.template_name, self.get_context)


def _create_user(email, first_name, second_name, password):
    user = User.objects.create_user(username=email,
                                    email=email, first_name=first_name,
                                    last_name=second_name, password=password)
    user.is_active = False
    user.save()

    return user


def _send_activation_email(user_email, user, request):
    current_site = get_current_site(request)
    message = render_to_string('activate_email.html', {
        'user': user, 'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    send('Happy Studio Account Activation', message, user_email)


def activate(request, uidb64, token):
    success_template_name = 'authentication/successful_activation.html'
    failure_template_name = 'authentication/failed_activation.html'

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        logger.info("Activated user with id " + str(uid))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        logger.warning("User doesn't exist but tried to activate account")

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, success_template_name, {})
    else:
        return render(request, failure_template_name, {})
