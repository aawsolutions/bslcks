from django.db import models
import os

class Category(models.Model):
    """Attachment Category model."""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

def generate_path(instance, filename):
    return os.path.join('attachments', instance.category.title, filename)

class Attachment(models.Model):
    file = models.FileField(upload_to=generate_path, blank=True) 
    file_date = models.DateTimeField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    protected = models.BooleanField(default=True)

    class META:
        ordering = ['file_date',]

    def __unicode__(self):
        if self.category:
            return u'%s - %s' % (self.category,self.file)
        else:
            return u'%s' % (self.file)
