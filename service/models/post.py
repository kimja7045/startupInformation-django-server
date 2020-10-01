from django.contrib.gis.db import models


class Post(models.Model):
    class Meta:
        verbose_name = '게시물'
        verbose_name_plural = verbose_name

    user = models.ForeignKey(
        to='User',
        verbose_name='작성자',
        related_name='posts',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='제목',
        max_length=64,
    )
    content = models.TextField(
        verbose_name='내용',
    )
    favorite_users = models.ManyToManyField(
        to='User',
        related_name='favorite_users',
        verbose_name='즐겨찾기한 사람들'
    )
    favorite_count = models.PositiveIntegerField(
        verbose_name='즐겨찾기 수',
        default=0
    )
    created_at = models.DateField(
        verbose_name='작성일',
        auto_now=True
    )
