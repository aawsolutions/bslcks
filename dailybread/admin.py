from django.contrib import admin
from dailybread.models import Devotion

class DevotionAdmin(admin.ModelAdmin):
    list_filter = ('date',)
admin.site.register(Devotion,DevotionAdmin)
