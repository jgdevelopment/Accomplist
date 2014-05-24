from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import main
from main import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
)