from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

class CheckEula(object):
    def process_request(self, request):
        if request.user.is_authenticated() and 'eula_accepted' \
            not in request.session and '/accounts/logout' not in request.path:
            try:
                request.user.groups.get(id=3)
                request.session["eula_accepted"] = True
            except ObjectDoesNotExist:
                from django.contrib.flatpages.models import FlatPage
                from django.template import RequestContext
                from django import forms
                from django.shortcuts import render_to_response
                from django.conf import settings

                class EulaForm(forms.Form):
                    accept = forms.BooleanField(required=False)

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
                            try:
                                p = request.user.get_profile()
                                if p.age < 13:
                                    message = 'Please have a parent or guardian contact <%s> to activate your account' % settings.ADMINS[0][1]
                                else:
                                    if accepted == True:
                                        try:
                                            request.user.groups.add(3)
                                            return HttpResponseRedirect('/')
                                        except ObjectDoesNotExist:
                                            message = 'Please contact <%s>, there has been a system error' % settings.ADMINS[0][1]
                                    else:
                                        message = 'You must accept the End User Licence Agreement to use the site while logged in.  If you do not wish to accept the agreement then you may log out and continue to use the public features'
                            except ObjectDoesNotExist:
                                message = 'This user account does not have a profile, please contact <%s>' % settings.ADMINS[0][1]
                else:
                    form = EulaForm()
                return render_to_response('accept-eula.html', {
                    'form': form,
                    'message': message,
                    'eula': eula,
                },context_instance=RequestContext(request))
