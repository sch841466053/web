# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-16 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0007_auto_20181016_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodscategory',
            name='parent_category',
        ),
    ]
