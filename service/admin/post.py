from django.contrib.gis import admin
from service.models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'created_at')
    search_fields = ('title', 'content')


@admin.register(Review)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('content',)
