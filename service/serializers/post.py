from rest_framework import serializers
from service.models import Post, Review, PublicPost, StartUpPlace
from service.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):  # 시리얼라이저(클라이언트에서 필요한 창업정보 데이터 리스트)
    has_favorite = serializers.SerializerMethodField(read_only=True)   # 이미 찜(즐겨찾기)했는지 유무 판단하는 변수
    user = UserProfileSerializer(read_only=True)    # 창업정보 게시물 작성자
    is_mine = serializers.SerializerMethodField(read_only=True)  # 내가 작성한 창업정보 게시물 유무 판단하는 변수
    favorite_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'image',
            'content',
            'favorite_count',
            'has_favorite',
            'is_mine',
            'created_at',
        )

    def get_favorite_count(self, obj):           # 찜(즐겨찾기) 개수 출력 함수
        return obj.favorite_users.count()

    def get_is_mine(self, obj):                  # 내가 작성한 창업정보 게시물 유무 판단하는 값 출력 함수
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.user_id == self.context['request'].user.id

    def get_has_favorite(self, obj):             # 이미 찜(즐겨찾기)한 게시물인지 유무 판단하는 값 출력 함수
        return self.context['request'].user.id in [favorite_user.id for favorite_user in obj.favorite_users.all()]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'content',
            'created_at',
        )


class PublicPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicPost
        fields = (
            'id',
            'title',
            'url',
            'created_at',
        )


class StartUpPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartUpPlace
        fields = (
            'id',
            'name',
            'enterprise',
            'address',
            'tel',
            'region',
            'latitude',
            'longitude',
        )
