from django.conf.urls.defaults import *
from django.views.generic import list_detail
from congregation.models import *

urlpatterns = patterns('congregation.views',
    url (r'^$',
        view='congregation_home',
        name='congregation_home'
    ),

    url(r'^households/$',
        view='household_list', 
        name='households_list'),

    url(r'^households/(?P<slug>[-\w]+)/$',
        view='household_detail',
        name='household_detail'
    ),

    url(r'^people/$',
        view='person_list',
        name='person_list'
    ),
    url(r'^people/(?P<slug>[-\w]+)/$',
        view='person_detail',
        name='person_detail'
    ),

    url(r'^groups/$',
        view='group_list',
        name='group_list'
    ),
    url(r'^groups/(?P<slug>[-\w]+)/$',
        view='group_detail',
        name='group_detail'
    ),

    url(r'^mailboxes/$',
        view='mailbox_list',
        name='mailbox_list'
    ),
    url(r'^mailboxes/(?P<slug>[-\w]+)/$',
        view='mailbox_detail',
        name='mailbox_detail'
    ),
    url(r'^talents/$',
        view='talents_list',
        name='talents_list'
    ),
    url(r'^talents/(?P<slug>[-\w]+)/$',
        view='talents_detail',
        name='talents_detail'
    ),
    url(r'^search/', view='search', name='congregation_search'),
)

