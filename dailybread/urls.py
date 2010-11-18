from django.conf.urls.defaults import *


urlpatterns = patterns('dailybread.views',
#    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
#        view='daily_bread_day',
#        name='devotional_day'
#    ),
#    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
#        view='daily_bread_archive_month',
#        name='devotional_archive_month'
#    ),
#    url(r'^(?P<year>\d{4})/$',
#        view='daily_bread_archive_year',
#        name='devotional_archive_year'
    url(r'^today/',
        view='daily_bread_today',
        name='get_daily_bread_today'),

    url(r'^scripture/(?P<reference>[^/]+)/$',
        view='scripture_reference',
        name='get_scripture'),
    url(r'^$',
        view='daily_bread_index',
        name='get_daily_bread_index'),


)

