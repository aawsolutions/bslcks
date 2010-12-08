from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from dailybread.models import Devotion
from basic.bookmarks.models import Bookmark
from sermons.models import Sermon

from apikeys.fetch import allkeys
from apikeys.models import Key

import datetime
import urllib

def ESVscripture(passage, domain):
    try:
       key = Key.objects.filter(vendor__name='ESV.org').filter(site__domain=domain)[0].key
    except:
       key = 'IP'
    return_options = [
        'include-short-copyright=0',
        'output-format=html',
        'include-passage-horizontal-lines=0',
        'include-heading-horizontal-lines=0']
    options = '&'.join(return_options)
    baseUrl = 'http://www.esvapi.org/v2/rest/passageQuery?key=%s' % (key)
    passage = passage.split()
    passage = '+'.join(passage)
    url = baseUrl + '&passage=%s&%s' % (passage, options)
    page = urllib.urlopen(url)
    return page.read()

class Daily:
    devotion = Devotion
    passage = '' 

def most_recent_devotion(request):
    passage = ''
    try:
        daily_devotion = Devotion.objects.filter(date__lte=datetime.date.today()).latest('date')
        dailybread = Daily()
        dailybread.devotion = daily_devotion
        dailybread.passage = ESVscripture(daily_devotion.scripture, request.META['HTTP_HOST'])

    except:
        dailybread = Devotion
        dailybread.scripture = 'error'
        dailybread.thoughts = 'No daily devotions found'

    return dailybread

def daily_bread_index(request):
    try:
        bookmarks = Bookmarks.objects.filter(tags__icontains='dailybread')
    except:
        bookmarks = []
    try:
        sermon = Sermons.objects.filter(date__lte=datetime.date.today()).latest('date')[0]
    except:
        sermon = []
    try:
        daily_devotions = Devotion.objects.filter(date__lte=datetime.date.today()).latest('date')
    except: 
        daily_devotions = []

    return render_to_response('dailybread_home.html', { 
        'devotion_bookmarks': bookmarks,
        'current_sermon': sermon,
        'dailybread': devotions,
        'keys': allkeys(request.META['HTTP_HOST']),
    }, context_instance=RequestContext(request))

def daily_bread_today(request):

    return render_to_response('dailybread.html', {
        'dailybread': most_recent_devotion(request),
        'keys': allkeys(request.META['HTTP_HOST']),
    }, context_instance=RequestContext(request))

def scripture_reference(request, reference):
    passage = reference
    
    dailybread = Daily()
    dailybread.passage = ESVscripture(reference, request.META['HTTP_HOST'])

    return render_to_response('dailybread.html', {
        'dailybread': dailybread,
        'keys': allkeys(request.META['HTTP_HOST']),
    }, context_instance=RequestContext(request))

