import uuid
import random
import string
import time
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from io import BytesIO
from PIL import Image
from service.utils import image as image_utils


class User(AbstractUser):
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = verbose_name

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='이메일'
    )
    nickname = models.CharField(
        null=True,
        max_length=30,
        verbose_name='닉네임'
    )
    phone_number = models.CharField(
        null=True,
        max_length=15,
        verbose_name='연락처'
    )
    image = models.ImageField(
        upload_to='profile_images',
        verbose_name='이미지',
        null=True,
        blank=True,
    )
    # is_approved = models.BooleanField(
    #     verbose_name='관리자 승인',
    #     default=False
    # )

    @classmethod
    def generate_username(cls):
        return ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(25)])

    def __str__(self):
        return f'{self.nickname}/{self.phone_number}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.image and not self.image.name.startswith('resized'):
            middle = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
            self.image.name = f'resized_{middle}_{int(time.time() * 100)}.{self.image.name.split(".")[-1]}'
            size = [700, 700]
            tmp = Image.open(BytesIO(self.image.read()))
            image = image_utils.rotate(tmp)
            self.image = image_utils.make_thumbnail(size, image, self.image.name)
        super().save()
