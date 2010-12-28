from django.contrib import admin
from sermons.models import *

class SermonAdmin(admin.ModelAdmin):
    list_filter = ('delivered', 'category',)
    ordering = ['-delivered',]
admin.site.register(Sermon, SermonAdmin)
