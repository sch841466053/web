# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-16 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0004_freecourse_seniorcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='birthday',
            field=models.DateField(blank=True, max_length=64, null=True, verbose_name='出生年月'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=32, null=True, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=64, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(max_length=11, null=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=64, null=True, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=32, null=True, verbose_name='姓名'),
        ),
    ]
