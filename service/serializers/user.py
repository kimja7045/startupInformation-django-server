from rest_framework import serializers

from service.exceptions import ValidationError
from service.models import *
from service.serializers import *
from datetime import date


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField()
    nickname = serializers.CharField()

    def signup(self):
        if User.objects.filter(email=self.data['email']).exists():
            raise ValidationError({'email': '이미 존재하는 이메일 입니다.'})
        if User.objects.filter(phone_number=self.data['phone_number']).exists():
            raise ValidationError({'phone_number': '이미 사용 중인 전화번호입니다.'})
        if User.objects.filter(nickname=self.data['nickname']).exists():
            raise ValidationError({'nickname': '이미 사용 중인 닉네임입니다.\n다른 닉네임을 입력해주세요.'})


        user = User.objects.create(
            username=User.generate_username(),
            phone_number=self.data['phone_number'], nickname=self.data['nickname'], email=self.data['email'],
        )
        user.set_password(self.data['password'])
        user.save()

        return user


class UserSignInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def signin(self):
        user = User.objects.filter(email=self.data['email']).first()
        if not user:
            raise ValidationError({'email': '가입되지 않는 이메일입니다.'})
        elif not user.check_password(self.data['password']):
            raise ValidationError({'password': '올바른 비밀번호를 입력해주세요.'})

        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'phone_number',
        )
