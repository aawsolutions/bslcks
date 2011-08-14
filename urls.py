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
    #(r'^mission/', include('basic.mission.urls')),
    (r'^places/', include('basic.places.urls')),
    (r'^dailybread/', include('dailybread.urls')),
    (r'^surveys/', include('survey.urls')),
    (r'^rss/', LatestNewsFeed()),
)


urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', name='accounts_login'),
    url(r'^accounts/logout/$', 'logout', {'next_page': '/',}),

    url(r'^accounts/password-change/$', 'password_change', name='password_change'),
    url(r'^accounts/password-change/success/$', 'password_change_done'),

    url(r'^accounts/password-reset/$', 'password_reset'),
    url(r'^accounts/password-reset/done/$', 'password_reset_done'),

    url(r'^accounts/password-reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'password_reset_complete'),


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

    url(r'^accounts/$',
        view='redirect_home')
)
