import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.conf import settings
from importlib import import_module
from portfolio.views import PortfolioView

test_email = "test@fakemail.com"
test_password = "test_password"


@pytest.fixture
@pytest.mark.django_db
def test_user():
    return User.objects.create_user(username=test_email, password=test_password, email=test_email)


@pytest.mark.django_db
@pytest.mark.parametrize(['user_mail', 'password', 'should_work'], [
    (test_email, test_password, True), (test_email+"spoiled", test_password, False),
    (test_email, test_password + "spoiled", False)
])
def test_login(user_mail, password, should_work, test_user):
    engine = import_module(settings.SESSION_ENGINE)
    session_key = None

    request = HttpRequest()
    request.META['HTTP_HOST'] = 'localhost'
    request.method = "post"
    request.session = engine.SessionStore(session_key)
    request.POST = {'user_email': user_mail, 'password': password}

    view = PortfolioView.as_view()
    response = view(request)

    if should_work:
        assert response.content == b''
    else:
        assert response.content != b''
    test_user.delete()
