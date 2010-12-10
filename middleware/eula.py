from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
 
class CheckEula(object):
    def process_request(self, request):
        if request.user.is_authenticated() and "eula_accepted" \
            not in request.session:
            try:
                request.user.groups.get(id=3)
                request.session["eula_accepted"] = True
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/accept-eula/')
