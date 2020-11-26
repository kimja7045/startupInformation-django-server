from rest_framework import serializers
from service.models import Post, Review
from service.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    has_favorite = serializers.SerializerMethodField(read_only=True)
    user = UserProfileSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)
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

    def get_favorite_count(self, obj):
        return obj.favorite_users.count()

    def get_is_mine(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.user_id == self.context['request'].user.id

    def get_has_favorite(self, obj):
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
