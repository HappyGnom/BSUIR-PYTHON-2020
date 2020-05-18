from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.NewsView.as_view(), name="news"),
    path('edit/<int:thread_id>/<int:news_id>', views.EditView.as_view(), name="news-edit")
]
