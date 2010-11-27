from django.db import models

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/', blank=True) 
    file_date = models.DateTimeField()
    description = models.TextField(blank=True)

    class META:
        ordering = ['file_date',]

    def __unicode__(self):
        return u'%s - %s' % (self.file,self.delivered.strftime('%m/%d/%Y @%I:%M%p '))
