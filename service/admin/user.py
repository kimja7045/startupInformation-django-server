from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin

from service.models.user import *


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'profile_image',)}),
    )
