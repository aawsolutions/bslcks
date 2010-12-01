from django.db import models
from django.forms import ModelForm

from congregation.models import Person

class ProfileForm(ModelForm):
    class META:
        model = Person
        exclude = ('slug', 'user', 'active', 'member', 'role', 'left', 'deceased', 'bslc_individual', )


