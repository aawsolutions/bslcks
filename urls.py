from django.conf.urls.defaults import *
from bslcks.feeds import LatestNewsFeed

#Admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

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

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', kwargs={'template_name': 'accounts/login.html',}, name='login'),
    url(r'^accounts/logout/$', 'logout', kwargs={'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^accounts/pwchange/$', 'password_change', kwargs={'template_name': 'accounts/pwchange.html'}, name='change_password'),
    url(r'^accounts/pwchange/success/$', 'password_change_done', kwargs={'template_name': 'accounts/success.html'}, name='password_change_success')
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
