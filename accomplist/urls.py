from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import projects
from projects import urls
import main
from main import urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'accomplist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include(projects.urls)),
    url(r'^', include(main.urls)),

)
