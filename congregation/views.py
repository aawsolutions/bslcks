from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail
from django.template import RequestContext
from congregation.models import *

from apikeys.fetch import allkeys

@login_required
def congregation_home(request, **kwargs):

    message = 'Hello World'
    return render_to_response('congregation/congregation_home.html', {
        'Message': message,
        'keys': allkeys(request.META['HTTP_HOST']),
    },context_instance=RequestContext(request))

@login_required
def talents_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Talents.objects.all(),
        paginate_by=paginate_by,
        **kwargs
    )

@login_required
def household_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Household.objects.all(),
        paginate_by=paginate_by,
        **kwargs
    )

@login_required
def person_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Person.objects.all(),
        paginate_by=paginate_by,
        **kwargs
    )

@login_required
def group_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Group.objects.filter(active=True),
        paginate_by=paginate_by,
        **kwargs
    )

@login_required
def mailbox_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Mailbox.objects.all(),
        paginate_by=paginate_by,
        **kwargs
    )

@login_required
def talents_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Talents.objects.all(),
        slug=slug,
        **kwargs
    )

@login_required
def household_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Household.objects.all(),
        slug=slug,
        **kwargs
    )

@login_required
def person_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Person.objects.all(),
        slug=slug,
        **kwargs
    )

@login_required
def group_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Group.objects.all(),
        slug=slug,
        **kwargs
    )

@login_required
def mailbox_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Mailbox.objects.all(),
        slug=slug,
        **kwargs
    )
