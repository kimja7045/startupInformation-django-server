from rest_framework import viewsets, pagination
from service.authentication import BaseSessionAuthentication
from service.models import Post
from service.serializers import PostSerializer


class PostPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        BaseSessionAuthentication,
    )
    queryset = Post.objects.all()
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
