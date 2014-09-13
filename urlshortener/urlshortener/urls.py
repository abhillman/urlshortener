from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('', 
    url(r'^$', views.CreateShortURL.as_view(), name='create-short-url'),
    url(r'^(?P<short_url>[a-zA-Z0-9]+)/$', views.resolve_short_url, name='resolve-short-url'), 
    url(r'^_admin/', include(admin.site.urls)),
)
