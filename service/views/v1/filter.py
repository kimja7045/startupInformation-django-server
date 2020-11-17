from django_filters import rest_framework as filters, CharFilter
from service.exceptions import ValidationError
from service.models import *
import datetime
import django_filters


class PostFilter(filters.FilterSet):
    keyword = CharFilter(method='get_keyword')

    class Meta:
        model = Post
        fields = (
            'keyword',
        )

    def get_keyword(self, queryset, name, value):
        return queryset.filter(
            title__contains=value
        ).distinct()
