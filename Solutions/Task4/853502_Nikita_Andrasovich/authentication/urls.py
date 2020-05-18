from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'authentication'
urlpatterns = [
    path('registration/', views.RegisterView.as_view(), name="registration"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
