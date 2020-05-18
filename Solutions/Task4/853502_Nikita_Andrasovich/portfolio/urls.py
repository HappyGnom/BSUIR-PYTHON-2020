from django.urls import path

from . import views

app_name = 'portfolio'
urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.PortfolioView.as_view(), name="portfolio"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
