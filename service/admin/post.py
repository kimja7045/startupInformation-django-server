from django.contrib.gis import admin
from service.models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content',)
    search_fields = ('title',)
