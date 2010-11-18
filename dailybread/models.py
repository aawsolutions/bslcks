from django.db import models

class Devotion(models.Model):
    date = models.DateField(unique=True)
    scripture = models.CharField("Eg. John3:1-3:16", max_length=100)
    thoughts = models.TextField()
    
    def __unicode__(self):
        return "%s (%s) - %s" % (self.date,self.date.strftime('%a'),self.scripture)

    class Meta:
        ordering = ('-date',)

    def save(self, *args, **kwargs):
        self.scripture = self.scripture.replace(u'\u2013','-')
        super(Devotion, self).save(*args, **kwargs) # Call the "real" save() method.
