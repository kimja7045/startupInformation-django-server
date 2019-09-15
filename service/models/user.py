import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models


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
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    profile_image = models.URLField(
        null=True,
        blank=True,
    )

    @classmethod
    def generate_username(cls):
        return ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(20)])

    @classmethod
    def generate_email(cls, username):
        return f'{username}@gonguhada.com'
