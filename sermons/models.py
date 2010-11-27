from django.db import models
from syncr.youtube.models import Video

class Sermon(models.Model):
    audio_file = models.FileField(upload_to='sermons/', blank=True) 
    youtube = models.ForeignKey(Video, blank=True, null=True)
    delivered = models.DateTimeField()
    text = models.TextField(blank=True)

    class META:
        ordering = ['delivered',]

    def __unicode__(self):
        return self.delivered.strftime('%m/%d/%Y @%I:%M%p ')

        
