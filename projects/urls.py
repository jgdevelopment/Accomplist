from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'accomplist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/', views.create_project, name='create_project'),
)
