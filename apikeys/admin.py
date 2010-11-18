from django.contrib import admin
from apikeys.models import *

class VendorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
admin.site.register(Vendor, VendorAdmin)

class KeyAdmin(admin.ModelAdmin):
    list_filter = ('vendor', 'site',)
admin.site.register(Key, KeyAdmin)
