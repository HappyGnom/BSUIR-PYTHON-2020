from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('', include('portfolio.urls')),
    path('news/', include('news.urls')),
    path('authentication/', include('authentication.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
     urlpatterns += [
         url(r'^media/(?P<path>.*)$', serve, {
             'document_root': settings.MEDIA_ROOT,
         })
     ]