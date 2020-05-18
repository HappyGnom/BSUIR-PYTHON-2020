import pytest
from news.views import NewsView, News, NewsThread, NewsSubscription, EditView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpRequest
from django.conf import settings
from importlib import import_module
from portfolio.views import PortfolioView
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


test_email = "test@fakemail.com"
test_password = "test_password"


@pytest.fixture
@pytest.mark.django_db
def test_user():
    return User.objects.create_user(username=test_email, password=test_password, email=test_email)


@pytest.mark.django_db
def test_news_access(test_user):
    test_thread_name = "ThreadName"
    thread = NewsThread(thread_name=test_thread_name)
    thread.save()

    test_title = "TestNews"
    test_content = "TestContent"

    news = News(title=test_title, pub_date=timezone.now(),
                content=test_content, thread=thread)
    news.save()

    subscription = NewsSubscription(user=test_user, thread=thread)
    subscription.save()

    request = HttpRequest()
    request.META['HTTP_HOST'] = 'localhost'
    request.method = "get"
    request.user = test_user

    view = NewsView.as_view()
    response = view(request)

    assert test_thread_name in response.content.decode('utf-8')
    assert test_title in response.content.decode('utf-8')

    subscription.delete()
    news.delete()
    thread.delete()
    test_user.delete()


@pytest.mark.django_db
def test_news_edit(test_user):
    test_thread_name = "ThreadName"
    thread = NewsThread(thread_name=test_thread_name)
    thread.save()

    test_title = "TestNews"
    test_content = "TestContent"

    news = News(title=test_title, pub_date=timezone.now(),
                content=test_content, thread=thread)
    news.save()

    request = HttpRequest()
    request.META['HTTP_HOST'] = 'localhost'
    request.method = "get"
    request.user = test_user
    
    view = EditView.as_view()
    response = view(request,news_id = news.pk, thread_id = thread.pk)

    assert "You are not authenticated as a manager." in response.content.decode(
        'utf-8')

    manager_group = Group.objects.create(name='manager')
    manager_group.user_set.add(test_user)
    manager_group.save()

    response = view(request,news_id = news.pk, thread_id = thread.pk)

    assert test_thread_name in response.content.decode('utf-8')
    assert test_title in response.content.decode('utf-8')

    manager_group.delete()
    news.delete()
    thread.delete()
    test_user.delete()
