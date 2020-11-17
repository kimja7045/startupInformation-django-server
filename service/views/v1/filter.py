from django_filters import rest_framework as filters, CharFilter
from service.exceptions import ValidationError
from service.models import *
import datetime
import django_filters


class PostFilter(filters.FilterSet):
    keyword = CharFilter(method='get_keyword')
    favorite_user = CharFilter(method='get_favorite_user')

    class Meta:
        model = Post
        fields = (
            'keyword',
            'user',
            'favorite_user',
        )

    def get_keyword(self, queryset, name, value):
        return queryset.filter(
            title__contains=value
        ).distinct()

    def get_favorite_user(self, queryset, name, value):
        return queryset.filter(
            favorite_users=value,
        )
