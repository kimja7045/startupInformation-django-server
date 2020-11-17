from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, filters
from service.authentication import BaseSessionAuthentication
from service.models import Post, Review
from service.serializers import PostSerializer, ReviewSerializer
from service.views.v1.filter import PostFilter
from rest_framework.decorators import action
from rest_framework.response import Response


class ContentPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        BaseSessionAuthentication,
    )
    queryset = Post.objects.all()
    pagination_class = ContentPagination
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = PostFilter

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(methods=['get'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        post.favorite_users.add(request.user)
        post.save()
        return Response({'code': 'OK'})

    @action(methods=['get'], detail=True)
    def unfavorite(self, request, pk=None):
        post = self.get_object()
        post.favorite_users.remove(request.user)
        post.save()
        return Response({'code': 'OK'})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user')
    authentication_classes = (
        BaseSessionAuthentication,
    )
    serializer_class = ReviewSerializer
    pagination_class = ContentPagination

    def get_queryset(self):
        return super().get_queryset().filter(post=self.kwargs['post_pk']).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs['post_pk'])

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
