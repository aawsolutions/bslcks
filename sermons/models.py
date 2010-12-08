from django.db import models

class Sermon(models.Model):
    audio_file = models.FileField(upload_to='sermons/', blank=True) 
    video = models.URLField(blank=True, null=True)
    delivered = models.DateTimeField()
    text = models.TextField(blank=True)

    class META:
        ordering = ['delivered',]

    def __unicode__(self):
        return self.delivered.strftime('%m/%d/%Y @%I:%M%p ')

        
