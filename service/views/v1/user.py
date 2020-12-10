import json
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, pagination, views, permissions
from rest_framework.response import Response
from service.models import *
from service.serializers import *
from django.contrib.auth import logout, login
from service.decorators import form_validation, required_fields, sms_verification
from service.authentication import BaseSessionAuthentication
from service.views.v1.filter import *


def logout_view(request):
    logout(request)
    return JsonResponse({'code': 'OK'})


class UserSignUpView(views.APIView):
    authentication_classes = (
        BaseSessionAuthentication,
    )

    def post(self, request):
        data = json.loads(request.body)

        if User.objects.filter(email=data['email']).exists():
            return JsonResponse(data={
                'code': 'exists',
                'msg': '이미 존재하는 이메일입니다.'
            }, status=400)
        elif User.objects.filter(phone_number=data['phone_number']).exists():
            return JsonResponse(data={
                'code': 'exists',
                'msg': '이미 사용 중인 전화번호입니다.'
            }, status=400)
        elif User.objects.filter(nickname=data['nickname']).exists():
            return JsonResponse(data={
                'code': 'exists',
                'msg': '이미 사용 중인 닉네임입니다.\n다른 닉네임을 입력해주세요.'
            }, status=400)

        user = User.objects.create(
            username=User.generate_username(),
            phone_number=data['phone_number'], nickname=data['nickname'], email=data['email'],
        )
        user.set_password(data['password'])
        user.save()

        login(request, user)
        return Response({'code': 'OK'})


class UserSignInView(views.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        logout(request)

        if request.user.is_authenticated:
            return JsonResponse({'code': 'OK'})

        data = json.loads(request.body)

        user = User.objects.filter(email=data['email']).first()
        if not user:
            return JsonResponse(data={
                'code': 'NotLogin',
                'msg': '사용자를 찾을 수 없습니다'
            }, status=400)
        elif not user.check_password(data['password']):
            return JsonResponse(data={
                'code': 'NotLogin',
                'msg': '올바른 비밀번호를 입력해주세요'
            }, status=400)
        login(request, user)
        serializer = UserProfileSerializer(instance=request.user)
        return JsonResponse(serializer.data)


class UserProfileView(views.APIView):
    authentication_classes = (
        BaseSessionAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)

        request.session.set_expiry(86400)
        return Response(serializer.data)

    @form_validation(UserProfileSerializer)
    def patch(self, request, serializer):
        serializer.instance = request.user
        serializer.save()
        return Response(serializer.data)
