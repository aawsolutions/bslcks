from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site

class Vendor(models.Model):
    name = models.CharField('api vendor', max_length=100, unique = True)

    def __unicode__(self):
        return '%s' % self.name

class Key(models.Model):
    vendor = models.ForeignKey(Vendor)
    site = models.ManyToManyField(Site)
    key = models.CharField(max_length=250, unique = True)

    def site_name(self):
        if self.site.count() > 1:
           return 'Multiple Sites'
        else:
           return self.site.values()[0]['name']

    def __unicode__(self):
        return '%s - %s' %  (self.vendor, self.site_name())

    class Meta:
        unique_together = (("key", "vendor"),)
        ordering = ['vendor', ]

