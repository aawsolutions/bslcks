from django.conf import settings
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Count
from django.contrib.localflavor.us.models import *
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.signals import request_finished

import re
from datetime import datetime
from dateutil.relativedelta import *

from photologue.models import Photo

class UserLogin(models.Model):
    """Represent users' logins, one per record"""
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        try:
            p = self.user.get_profile()
            return u'%s on %s' % (p, self.timestamp)
        except:
            return u'%s on %s' % (self.user, self.timestamp) 

@receiver(pre_save, sender=User, dispatch_uid='LoginCounter')
def user_presave(sender, instance, **kwargs):
    try:
        if instance.last_login:
            old = instance.__class__.objects.get(pk=instance.pk)
            if instance.last_login != old.last_login:
                instance.userlogin_set.create(timestamp=instance.last_login)
    except:
        pass


class Talents(models.Model):
    name = models.CharField('talent name', max_length=100)
    slug = models.SlugField('slug', unique=True)
    category = models.ForeignKey('self', blank=True, null=True, related_name='sub-category')

    class Meta:
        verbose_name = 'talent'
        verbose_name_plural = 'talents'
        ordering = ('name',)

class Role(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField('slug', unique=True)
    

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        ordering = ('name',)     


class Household(models.Model):
    name = models.CharField('household name', max_length=100)
    slug = models.SlugField('slug', unique=True)
    address = models.CharField('physical address', max_length=100)
    apartment = models.CharField('apartment/unit number', blank=True, max_length=10)
    zipcode = models.CharField('5 digit zip code', max_length=5)
    state = USStateField('state')
    household_phone = PhoneNumberField('household phone', blank=True)
    unlisted_number = models.BooleanField(default=False)
    bslc_household = models.IntegerField('BSLC DB Household #', blank=True, unique=True)
    picture = models.ForeignKey(Photo, blank=True, null=True)

    class Meta:
        verbose_name = 'household'
        verbose_name_plural = 'households'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def last_name(self):
        lname = re.search(r'[^ ]*$',self.name)
        return self.name[lname.start():lname.end()]

    @permalink
    def get_absolute_url(self):
        return ('household_detail', None, {'slug': self.slug}) 

    @property
    def full_address(self):
        addy = ''
        if self.address:
            addy += self.address
            addy += ' '
        if self.apartment:
            addy += self.apartment
            addy += ', '
        else:
            addy += ', '
        if self.zipcode:
            addy += self.zipcode
        return addy

class Prefix(models.Model):
    prefix = models.CharField(max_length=20)
    initials = models.CharField(max_length=5)

    def __unicode__(self):
        return u'%s (%s)' % (self.initials.capitalize(),self.prefix.capitalize())

class Person(models.Model):
    """Person model."""
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    prefix = models.ForeignKey('prefix', blank=True, null=True)
    first_name = models.CharField('first name', blank=True, max_length=100)
    preferred_first_name = models.CharField(blank=True, max_length=100)
    middle_name = models.CharField('middle name', blank=True, max_length=100)
    last_name = models.CharField('last name', blank=True, max_length=100)
    suffix = models.CharField('suffix', max_length=10, blank=True)

    slug = models.SlugField('slug', unique=True)
    user = models.ForeignKey(User, blank=True, null=True, help_text='If the person is an existing site user')

    gender = models.CharField('gender',choices=GENDER_CHOICES, max_length=1)
    birth_date = models.DateField('birth date', blank=True, null=True)
    baptism_date = models.DateField('baptism date', blank=True, null=True)

    active = models.BooleanField(default=True)
    member = models.BooleanField(default=True)
    role = models.ManyToManyField(Role, blank=True, null=True)
    opt_in_directory = models.BooleanField('opt-in to directory', default=True)
    directory_report_order = models.IntegerField(blank=True, null=True)

    joined = models.DateField('member since', blank=True, null=True)
    left = models.DateField('left on', blank=True, null=True)

    talents = models.ManyToManyField(Talents, blank=True, null=True)

    relations = models.ManyToManyField("self", blank=True, null=True)
    household = models.ForeignKey(Household, blank=True, null=True)

    bio = models.TextField('biography', blank=True)
    picture = models.ForeignKey(Photo, blank=True, null=True)

    email = models.EmailField(blank=True)
    landline = PhoneNumberField('landline phone', blank=True)
    cellphone = PhoneNumberField('cell phone', blank=True)

    deceased = models.DateField(null=True, blank=True)

    bslc_individual = models.CharField('BSLC DB Individual #', blank=True, null=True, max_length=15, unique=True)

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'people'
        ordering = ('last_name', 'first_name',)
        unique_together = ('last_name', 'first_name', 'user')

    def __unicode__(self):
        return u'%s' % self.full_name

    def save(self, *args, **kwargs):
        try:
            self.user.email = self.email
            self.user.save()
        except:
            pass
        super(Person, self).save(*args, **kwargs) # Call the "real" save() method.

    @property
    def full_name(self):
        if self.preferred_first_name:
            return u'%s %s' % (self.preferred_first_name, self.last_name)
        else:
            return u'%s %s' % (self.first_name, self.last_name)

    @property
    def age(self):
        if self.birth_date:
            TODAY = datetime.today()
            return relativedelta(TODAY, self.birth_date).years
        else:
            return
    
    @property
    def age_days(self):
        if self.birth_date:
            TODAY = datetime.today().date()
            diff = TODAY - self.birth_date
            return diff.days
        else:
            return

    @permalink
    def get_absolute_url(self):
        return ('person_detail', None, {'slug': self.slug}) 

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Person.objects.create(user=instance)

#post_save.connect(create_user_profile, sender=User)

class GroupType(models.Model):
    name = models.CharField('group type name', max_length=100)
    slug = models.SlugField('slug', unique=True)

    def __unicode__(self):
        return '%s' % self.name

class Group(models.Model):
    name = models.CharField('group name', max_length=100)
    slug = models.SlugField('slug', unique=True)
    gtype = models.ForeignKey(GroupType, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.ForeignKey(Photo, blank=True, null=True)
    leaders = models.ManyToManyField(Person, related_name='leaders')
    members = models.ManyToManyField(Person, related_name='members', blank = True, null = True)

    talents = models.ManyToManyField(Talents, blank=True)

    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('group_detail', None, {'slug': self.slug})


class Mailbox(models.Model):
    number = models.IntegerField(unique=True)
    occupants = models.ManyToManyField(Person)

    class Meta:
        verbose_name = 'mailbox'
        verbose_name_plural = 'mailboxes'
        ordering = ('number',)

    def occupants_list(self):
        names = ''
        occs = self.occupants.order_by('birth_date').values_list('first_name', 'last_name')
        thecount = 1
        themax = len(occs)

        for occupant in occs:
            names += '%s %s' % (occupant[0], occupant[1])
            if thecount < themax:
               names += ', '
               if (themax-1) == thecount:
                   names += ' and '
            thecount +=1
        return names

    @property
    def num_occupants(self):
        return self.occupants.count()

    def __unicode__(self):
        return '%s - %s (%s)' %  (self.number, self.num_occupants, self.occupants_list())

