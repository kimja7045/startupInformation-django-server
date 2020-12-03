from django_filters import rest_framework as filters, CharFilter
from service.exceptions import ValidationError
from service.models import *
import datetime
import django_filters


class PostFilter(filters.FilterSet): # 창업정보 게시물 필터 클래스
    keyword = CharFilter(method='get_keyword')   # 창업정보 게시물 제목 값
    favorite_user = CharFilter(method='get_favorite_user')   # 찜(즐겨찾기)한 유저 값

    class Meta:
        model = Post  # 창업정보 게시물
        fields = (
            'keyword',  # 창업정보 게시물 키워드(제목)
            'user',     # 창업정보 게시물 작성자
            'favorite_user', # 찜(즐겨찾기)한 유저 값
        )

    def get_keyword(self, queryset, name, value):  # queryset = Post(창업정보 게시물), value = 검색 키워드
        return queryset.filter(
            title__contains=value  # 검색 키워드가 창업정보 게시물 키워드(제목)에 포함되는지 필터로 키워드가 포함되는 창업정보 게시물만 출력 = LIKE
        ).distinct()

    def get_favorite_user(self, queryset, name, value):  # value = user, 마이페이지에서 사용
        return queryset.filter(
            favorite_users=value,  # 찜(즐겨찾기)한 유저 리스트에 클라이언트가 포함되는지 필터로 확인 후 클라이언트가 찜한 창업정보 게시물만 출력
        )
