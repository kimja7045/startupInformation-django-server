from django.contrib.gis import admin
from service.models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'image', 'created_at')
    search_fields = ('title', 'content')


@admin.register(Review)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('content',)


@admin.register(PublicPost)
class PublicPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    search_fields = ('title', 'url', 'created_at')


@admin.register(StartUpPlace)
class StartUpPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'enterprise', 'tel', 'region')
    search_fields = ('name', 'enterprise', 'region', 'tel')
