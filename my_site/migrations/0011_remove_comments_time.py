# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-18 10:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0010_auto_20181018_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='time',
        ),
    ]