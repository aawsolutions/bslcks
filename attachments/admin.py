from django.contrib import admin
from attachments.models import *

class AttachmentAdmin(admin.ModelAdmin):
    list_filter = ('file_date',)
admin.site.register(Attachment, AttachmentAdmin)
