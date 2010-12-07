from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q

from django.views.generic import TemplateView

from datetime import date

from apikeys.fetch import allkeys
from dailybread.models import Devotion
from congregation.models import Person
from basic.blog.models import Post

def Homepage(request):
    motd = "Hello World!"

    try:
        dailybread = Devotion.objects.filter(date__lte=date.today()).latest('date')
    except:
        dailybread = Devotion
        dailybread.scripture = 'error'
        dailybread.thoughts = 'No daily devotions found'

    return render_to_response('homepage.html', {
        'motd': motd,
        'keys': allkeys(request.META['HTTP_HOST']),
        'dailybread': dailybread,
    },context_instance=RequestContext(request))

def Map(request):
    motd = 'Hello World'

    return render_to_response('map.html', {
        'motd': motd,
        'keys': allkeys(request.META['HTTP_HOST']),
    },context_instance=RequestContext(request))

def Staff(request):
    motd = 'Hello World'
    staffgroups = {}

    staff = Person.objects.filter(Q(members__name='Staff') | Q(leaders__name='Staff'))
    staffgroups[0] = staff.filter(leaders__name='Ordained Ministers').distinct()
    staffgroups[1] = staff.filter(members__name='Ordained Ministers').distinct()
    staff = staff.exclude(leaders__name='Ordained Ministers')
    staffgroups[2] = staff.filter(role__name__icontains='director').distinct()
    staff = staff.exclude(role__name__icontains='director')
    staffgroups[3] = staff.filter(role__name__icontains='senior').filter(role__name__icontains='assistant').distinct()
    staff = staff.exclude(role__name__icontains='senior')
    staffgroups[4] = staff.filter(role__name__icontains='assistant').exclude(role__name__icontains='senior').distinct()
    staff = staff.exclude(role__name__icontains='assistant')
    staffgroups[5] = staff.filter(role__name__icontains='coordinator').distinct()

    return render_to_response('staff.html', {
        'motd': motd,
        'keys': allkeys(request.META['HTTP_HOST']),
        'staffgroups': staffgroups,
    },context_instance=RequestContext(request))
