from service.models import *
from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    has_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'favorite_count'
            'has_favorite',
            'is_mine',
            'created_at',
        )

    def get_is_mine(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return obj.user_id == self.context['request'].user.id

    def get_has_liked(self, obj):
        return self.context['request'].user.id in [favorite_user for favorite_user in obj.favorite_users.all()]
