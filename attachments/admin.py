from django.contrib import admin
from attachments.models import *

class CategoryAdmin(admin.ModelAdmin):
    order_by = ('title',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin) 

class AttachmentAdmin(admin.ModelAdmin):
    list_filter = ('file_date','category', 'protected',)
admin.site.register(Attachment, AttachmentAdmin)
