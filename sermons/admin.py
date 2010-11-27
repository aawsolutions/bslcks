from django.contrib import admin
from sermons.models import *

class SermonAdmin(admin.ModelAdmin):
    list_filter = ('delivered',)
admin.site.register(Sermon, SermonAdmin)
