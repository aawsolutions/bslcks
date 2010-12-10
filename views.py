from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext
from django.db.models import Q
from django import forms
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

class EulaForm(forms.Form):
    accept = forms.BooleanField(required=False)

def accept_eula(request):
    from django.contrib.flatpages.models import FlatPage
    try:
        eula = FlatPage.objects.get(url='/eula/')
    except ObjectDoesNotExist:
        eula = []

    message = ''
    if request.method == 'POST':
        form = EulaForm(request.POST)
        if form.is_valid():
            accepted = form.cleaned_data['accept']
            if request.user.is_authenticated():
                if accepted == True:
                    try:
                        request.user.groups.add(3)
                        return HttpResponseRedirect('/')
                    except ObjectDoesNotExist:
                        message = 'Please contact <%s>, there has been a system error' % settings.ADMINS[0][1]
                else:
                    message = 'You must accept the End User Licence Agreement to use the site while logged in.  If you do not wish to accept the agreement then you may log out and continue to use the public features'
    else:
        form = EulaForm()
        message = 'There was an error processing your request.  Please try again'
    return render_to_response('accept-eula.html', {
        'form': form,
        'message': message,
        'eula': eula,
    },context_instance=RequestContext(request))


