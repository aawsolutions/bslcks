from django.db import models

class Sermon(models.Model):
    audio_file = models.FileField(upload_to='sermons/') 
    delivered = models.DateTimeField()
    text = models.TextField(blank=True)

    class META:
        ordering = ['delivered',]

    def __unicode__(self):
        return self.delivered.strftime('%m/%d/%Y @%I:%M%p ')

        
