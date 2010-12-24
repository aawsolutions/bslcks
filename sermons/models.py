from django.db import models
from basic.blog.models import Category

class Sermon(models.Model):
    audio_file = models.FileField(upload_to='sermons/', blank=True, help_text='an mp3 smaller than 10MB') 
    video = models.URLField(blank=True, null=True, help_text='a link to a video on youtube, vimeo, etc')
    delivered = models.DateTimeField(help_text='Date and time (24 hour clock) delivered, eg. 12/5/2010 at 10:45:00')
    category = models.ForeignKey(Category)
    text = models.TextField(blank=True, help_text='sermon transcript (markdown format preferred)')

    class META:
        ordering = ['delivered',]

    def __unicode__(self):
        return '%s - %s' % (self.category,self.delivered.strftime('%m/%d/%Y @%I:%M%p '))

        
