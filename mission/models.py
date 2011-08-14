from django.db import models
from basic.models import Place
from congregation.models import Person

# Create your models here.

Frequency_Choices = ('daily', 'weekly', 'monthly','yearly')


class Reoccurrance(models.Model):
    frequency = models.CharField(choices = Frequency_Choices)

class Event(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField()
    
    attendee = models.ManyToMany('Person')
    occurring = models.DateTimeField()
    place = modelsForeignKey('Place')
    reoccurring = models.ForeignKey('Reoccurrance', blank=True)
