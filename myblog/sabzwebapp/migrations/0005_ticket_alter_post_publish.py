# Generated by Django 5.1.2 on 2024-10-13 18:21

import datetime
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sabzwebapp', '0004_alter_post_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=250, verbose_name='متن')),
                ('name', models.CharField(max_length=50, verbose_name='نام')),
                ('email', models.EmailField(max_length=20, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=11, verbose_name='تلفن')),
                ('subject', models.CharField(max_length=250, verbose_name='موضوع')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2024, 10, 13, 18, 21, 0, 714343, tzinfo=datetime.timezone.utc), verbose_name='تاریخ انتشار'),
        ),
    ]