import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from authentication.views import RegisterView, activate
from authentication.forms import RegisterForm
from authentication.tokens import account_activation_token
from django.test import Client
from django.urls import reverse
from django.conf import settings
from importlib import import_module


@pytest.mark.django_db
def test_registration_activation():
    first_name = "Test Name"
    second_name = "Test Surname"
    email = 'test@fakemail.com'
    password = 'test_password'

    request = HttpRequest()
    request.method = "post"
    request.META['HTTP_HOST'] = 'localhost'
    request.POST = {'first_name': first_name, 'second_name': second_name,
                    'password': password, 'user_email': email}

    view = RegisterView.as_view()
    view(request)

    user = User.objects.get(username=email)

    assert user is not None
    assert user.email == email
    assert user.is_active is False

    activate(HttpRequest(), urlsafe_base64_encode(force_bytes(user.pk)),
             account_activation_token._make_token_with_timestamp(user, account_activation_token._num_days(
                 account_activation_token._today())))

    user = User.objects.get(username=email)
    assert user.is_active is True
    assert user.first_name == first_name

    user.delete()


@pytest.mark.django_db
def test_registration_duplicate():
    first_name = "Test Name"
    second_name = "Test Surname"
    email = 'test@fakemail.com'
    password = 'test_password'

    request = HttpRequest()
    request.method = "post"
    request.META['HTTP_HOST'] = 'localhost'
    request.POST = {'first_name': first_name, 'second_name': second_name,
                    'password': password, 'user_email': email}

    view = RegisterView.as_view()
    view(request)

    response = view(request)
    assert 'User for that email already exists!' in response.content.decode('utf-8')
