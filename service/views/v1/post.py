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
        BaseSessionAuthentication,        # 세션 유무 확인
    )
    queryset = Post.objects.all()         # 창업정보(게시물) 데이터 리스트 저장
    pagination_class = ContentPagination  # 페이지네이션 설정
    serializer_class = PostSerializer     # 시리얼라이저(클라이언트에서 필요한 창업정보 데이터 리스트) 설정
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 필터를 위한 라이브러리 설정
    filter_class = PostFilter             # 창업정보 제목, 작성자, 찜(즐겨찾기) 필터 알고리즘이 만들어진 소스 설정

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):   # 창업정보 업데이트 (제어 클래스 부분)
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
        return super().get_queryset().order_by('-id').distinct()


# 공공데이터(창업넷 공지사항 최신 100개) 가져오는 리스트 api
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

        xmlObject = xmltodict.parse(req)   # xml인 데이터 형식을 json 형태로 변환
        allData = xmlObject['response']['body']['items']['item']  # 공지사항 리스트 데이터(100개) 저장
        # print(allData)
        # print(allData[0]['title'])
        # print(allData[0]['detailurl'])
        # print(allData[0]['insertdate'])

        for notice_post in allData:
            PublicPost.objects.create(  # 필요한 데이터만 만들어둔 창업정보 게시물 모델(PublicPost)에
                title=notice_post['title'],  # 저장
                url=notice_post['detailurl'],
                created_at=notice_post['insertdate'],
            )

        return Response({'response': 'ok'})   # 에러 없이 수행됐을 시의 결과 출력
