from django.contrib import admin
from congregation.models import *

class TalentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Talents, TalentAdmin)

class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Role, RoleAdmin)

class HouseholdAdmin(admin.ModelAdmin):
    search_fields = ('name', 'bslc_household', )
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Household, HouseholdAdmin)

class PrefixAdmin(admin.ModelAdmin):
    search_fields = ('prefix',)
admin.site.register(Prefix, PrefixAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_filter = ('member','gender',)
    PhoneNumberField = ('deskphone','cellphone',)
    search_fields = ('first_name', 'last_name','preferred_first_name',)
    filter_horizontal = ('talents', 'relations')
    prepopulated_fields = {'slug': ('first_name','last_name'), 'preferred_first_name': ('first_name',)}
admin.site.register(Person, PersonAdmin)

class GroupTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(GroupType, GroupTypeAdmin)

class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('leaders', 'members', 'talents')
admin.site.register(Group, GroupAdmin)

class MailboxAdmin(admin.ModelAdmin):
    search_fields = ('number',)
admin.site.register(Mailbox, MailboxAdmin)

