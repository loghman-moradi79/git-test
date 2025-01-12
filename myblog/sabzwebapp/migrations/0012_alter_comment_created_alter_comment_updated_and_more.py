# Generated by Django 5.1.2 on 2024-10-15 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sabzwebapp', '0011_post_reading_time_alter_comment_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(verbose_name='تاریخ انتشار'),
        ),
        migrations.AlterField(
            model_name='post',
            name='reading_time',
            field=models.PositiveBigIntegerField(verbose_name='زمان مطالعه'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]
