from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin

from service.models import *


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'phone_number')}),
    )
    list_display = ('nickname', 'phone_number', 'email')
    search_fields = ('nickname', 'phone_number', 'email')
