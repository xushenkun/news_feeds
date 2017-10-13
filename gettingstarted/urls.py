from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
from hello.feeds import NeteaseFeed, NeteaseChannelFeed

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feed/163$', NeteaseChannelFeed()),
    url(r'^feed/163/(?P<tid>.*)$', NeteaseFeed()),
]
