from django.shortcuts import get_object_or_404, render_to_response, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail
from django.template import RequestContext
from django.forms import ModelForm

from congregation.models import *

from apikeys.fetch import allkeys

class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('slug','user','active','member', 'role', 'directory_report_order', 'left', 'household', 'picture', 'deceased', 'bslc_individual', 'relations', 'joined', 'talents')

class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        exclude = ('bslc_household', 'picture',)

@login_required
def congregation_home(request, **kwargs):
    

    return render_to_response('congregation/congregation_home.html', {
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
        queryset=Person.objects.exclude(deceased__isnull=False).exclude(active=False).exclude(opt_in_directory=False),
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
    try:
        h = Household.objects.get(slug=slug)
        people = h.person_set.exclude(deceased__isnull=False).exclude(active=False).exclude(opt_in_directory=False)
    except:
        people = None
    return list_detail.object_detail(
        request,
        queryset=Household.objects.all(),
        extra_context={'people': people,},
        slug=slug,
        **kwargs
    )

@login_required
def person_detail(request, slug, **kwargs):
    extra = {}
    if request.method == 'GET':
        person = request.user.get_profile()
        if person.slug == slug:
            if person.directory_report_order < 3:
                extra['household_edit'] = True
            extra['this_is_you'] = True
            extra['editme'] = request.GET.get('edit', False)
        return list_detail.object_detail(
            request,
            queryset=Person.objects.exclude(deceased__isnull=False).exclude(active=False).exclude(opt_in_directory=False),
            slug=slug,
            extra_context=extra,
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

# Stop Words courtesy of http://www.dcs.gla.ac.uk/idom/ir_resources/linguistic_utils/stop_words
STOP_WORDS = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|
although|always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|
around|as|at|back|be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|
besides|between|beyond|bill|both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|
detail|do|done|down|due|during|each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|
everything|everywhere|except|few|fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|
front|full|further|get|give|go|had|has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|
him|himself|his|how|however|hundred|i|ie|if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|
least|less|ltd|made|many|may|me|meanwhile|might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|
namely|neither|never|nevertheless|next|nine|no|nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|
one|only|onto|or|other|others|otherwise|our|ours|ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|
see|seem|seemed|seeming|seems|serious|several|she|should|show|side|since|sincere|six|sixty|so|some|somehow|someone|
something|sometime|sometimes|somewhere|still|such|system|take|ten|than|that|the|their|them|themselves|then|thence|
there|thereafter|thereby|therefore|therein|thereupon|these|they|thick|thin|third|this|those|though|three|through|
throughout|thru|thus|to|together|too|top|toward|towards|twelve|twenty|two|un|under|until|up|upon|us|very|via|was|
we|well|were|what|whatever|when|whence|whenever|where|whereafter|whereas|whereby|wherein|whereupon|wherever|whether|
which|while|whither|who|whoever|whole|whom|whose|why|will|with|within|without|would|yet|you|your|yours|yourself|
yourselves)\b"""

@login_required
def search(request, template_name='congregation/search_results.html'):
    """
    Search the congregation.

    This template will allow you to setup a simple search form that will try to return results based on
    given search strings. The queries will be put through a stop words filter to remove words like
    'the', 'a', or 'have' to help imporve the result set.

    Template: ``congregation/search.html``
    Context:
        object_list
            List of people that match given search term(s).
        search_term
            Given search term.
    """
    context = {}
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
        search_term = '%s' % request.GET['findperson']
        cleaned_search_term = stop_word_list.sub('', search_term)
        cleaned_search_term = cleaned_search_term.strip()
        terms = cleaned_search_term.split(' ')
        if len(cleaned_search_term) != 0:
            people_list = Person.objects.filter(
                Q(first_name__icontains=cleaned_search_term) | 
                Q(last_name__icontains=cleaned_search_term) | 
                Q(preferred_first_name__icontains=cleaned_search_term) 
            )
            if len(people_list) < 1:
                people_list = Person.objects.filter(
                    Q(first_name__iregex=r'(' + '|'.join(terms) + ')') | Q(preferred_first_name__iregex=r'(' + '|'.join(terms) + ')')
                    ).filter(last_name__iregex=r'(' + '|'.join(terms) + ')')
                if len(people_list)<1:
                    message = 'no match found for '
                else:
                    message = 'matches found for '
            else:
                message = 'matches found for '

            people_list = people_list.exclude(deceased__isnull=False).exclude(active=False).exclude(opt_in_directory=False)
            context = {'object_list': people_list, 'message': message, 'search_term':search_term, }
        else:
            message = 'Search term was too vague. Please try again.'
            context = {'message':message}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
def profile_manager(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(person_detail, args=(request.user.get_profile().slug,)))

    else:
        person = request.user.get_profile()
        form = PersonForm(instance=person)

    return render_to_response('congregation/profile_manager.html', {
        'form': form,
    },context_instance=RequestContext(request))

@login_required
def household_manager(request):
    person = request.user.get_profile()
    if person.directory_report_order < 3:
        if request.method == 'POST':
            form = HouseholdForm(request.POST, instance=person.household)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(household_detail, args=(person.household.slug,)))
    
        else:
            household = person.household
            form = HouseholdForm(instance=household)
    
        return render_to_response('congregation/profile_manager.html', {
            'form': form,
        },context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse(household_detail, args=(person.household.slug,)))

