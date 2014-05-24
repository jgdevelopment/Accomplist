from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from accounts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create_account/', views.create_account, name='create_account'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout')
)