from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import Review, Project
from .forms import ClientEmailForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PortfolioView(generic.View):
    template_name = 'portfolio/home.html'
    context_object_name = 'context'

    def get_context(self, **kwargs):
        context = {}
        context['top_reviews'] = Review.objects.order_by('-rating')[:4]
        context['our_projects'] = Project.objects.all()
        context['client_mail_form'] = ClientEmailForm()
        context['login_form'] = LoginForm()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'password' in request.POST:
            login_form = LoginForm(self.request.POST)
            if login_form.is_valid():
                user_email = login_form.cleaned_data['user_email']
                password = login_form.cleaned_data['password']

                user = authenticate(
                    request, username=user_email, password=password)
                if user is not None:
                    login(request, user)
                    logger.info("Logged in user " + user_email)
                    return HttpResponseRedirect('news/')
                else:
                    logger.info("Wrong data authentication")
                    return render(request, self.template_name, {**self.get_context(), 'auth_failed': True})
        else:
            client_email_form = ClientEmailForm(self.request.POST)
            if client_email_form.is_valid():
                client_mail = client_email_form.cleaned_data['client_email']

                send_mail('Happy Studio Request', 'Hello, I would like to work together with Happy Studio! Please, contact me using this email: ' +
                          client_mail, 'andrasovi4@gmail.com', ['andrasovi4@gmail.com'], fail_silently=False,)

                request.session['email'] = client_mail
                logger.info("Sent 'contact us' email")
                return HttpResponseRedirect('contact/')


class ContactView(generic.CreateView):
    template_name = 'portfolio/contact.html'
    context_object_name = 'context'

    def get(self, request, *args, **kwargs):
        if request.session.has_key('email'):
            return render(request, self.template_name, {'email': request.session.get('email')})
        else:
            return render(request, self.template_name, {'email': None})
