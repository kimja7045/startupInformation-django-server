# Generated by Django 2.2.12 on 2020-10-01 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_post_favorite_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favorite_count',
            field=models.PositiveIntegerField(default=0, verbose_name='즐겨찾기 수'),
        ),
    ]
