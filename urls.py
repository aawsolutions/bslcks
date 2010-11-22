from django.conf.urls.defaults import *
from bslcks.feeds import LatestNewsFeed

#Admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),

    (r'^photos/', include('photologue.urls')),
    (r'^congregation/', include('congregation.urls')),

    (r'^news/',      include('basic.blog.urls')),
    (r'^bookmarks/', include('basic.bookmarks.urls')),
    (r'^comments/', include('basic.comments.urls')),
    (r'^events/', include('basic.events.urls')),
    (r'^places/', include('basic.places.urls')),

    (r'^dailybread/', include('dailybread.urls')),

    (r'^rss/', LatestNewsFeed()),
)

urlpatterns += patterns('bslcks.views',
    url(r'^$',
        view='Homepage',
        name='home'),


    url(r'^map/',
        view='Map',
        name='map'),


    url(r'^staff/',
        view='Staff',
        name='staff'),

)
