# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-16 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0006_auto_20181016_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodscategory',
            name='category',
            field=models.CharField(choices=[(1, '一级类'), (2, '二级类'), (3, '三级类')], max_length=32, null=True, verbose_name='商品类录级别'),
        ),
        migrations.AddField(
            model_name='goodscategory',
            name='parent_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_site.GoodsCategory', verbose_name='父类目级别'),
        ),
        migrations.AlterField(
            model_name='goodscategory',
            name='name',
            field=models.CharField(max_length=32, verbose_name='商品类名'),
        ),
    ]
