from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'accomplist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/', views.create_project, name='create_project'),
    url(r'view/(?P<slug>[\w-]+)', views.view_project, name='view_project'),
    url(r'^addtask/', views.add_task, name='add_task'),
    url(r'^gettasks/', views.get_tasks, name='get_tasks'),
)
