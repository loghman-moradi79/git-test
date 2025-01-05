# Generated by Django 5.1.2 on 2024-10-13 13:00

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sabzwebapp', '0002_alter_post_author_alter_post_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2024, 10, 13, 13, 0, 1, 533135, tzinfo=datetime.timezone.utc), verbose_name='تاریخ انتشار'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]
