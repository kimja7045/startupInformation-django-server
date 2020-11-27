from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, filters
from service.authentication import BaseSessionAuthentication
from service.models import Post, Review, PublicPost
from service.serializers import PostSerializer, ReviewSerializer, PublicPostSerializer
from service.views.v1.filter import PostFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import json
import xmltodict


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
        # serializer.save(user=self.request.user, post_id=self.kwargs['post_pk'])
        serializer.save(user=self.request.user, post_id=self.kwargs['post_pk'])

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class PublicPostViewSet(viewsets.ModelViewSet):
    # authentication_classes = (
    #     BaseSessionAuthentication,
    # )
    queryset = PublicPost.objects.all()
    serializer_class = PublicPostSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('id').distinct()


# 공공데이터(창업넷 공지사항 최신 100개) api
class OpenPostView(APIView):
    def get(self, request):
        # numOfRows: 페이지당 게시물 목록 수
        # startPage : 시작페이지 번호
        # pageSize : 페이지당 게시물 목록 건수
        # pageNo : 페이지번호

        req = requests.get('http://openapi.kised.or.kr/openapi/service/rest/ContentsService/getNoticeList?'
                           'serviceKey=UO7tvHBrpODqQ%2BFLE4u3%2FRWyekRHkB5tnV%2B3OS2FaYJeT8xLTF2d5Qa7xH6y32xBp9BJR5eex%2FOPNb0s0zpfeg%3D%3D'
                           '&numOfRows=100'
                           '&startPage=1'
                           '&pageSize=100'
                           '&pageNo=1').content

        xmlObject = xmltodict.parse(req)
        allData = xmlObject['response']['body']['items']['item']
        # print('\n\n\n')
        # print(allData[0]['title'])
        # print(allData[0]['detailurl'])
        # print(allData[0]['insertdate'])

        for notice_post in allData:
            PublicPost.objects.create(
                title=notice_post['title'],
                url=notice_post['detailurl'],
                created_at=notice_post['insertdate'],
            )
        # print(allData)

        return Response({'response': 'ok'})
