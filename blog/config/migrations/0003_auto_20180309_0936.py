# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-09 01:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_sidebar_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='content',
            field=models.CharField(blank=True, help_text='\u975eHTML\u7c7b\u578b\uff0c\u53ef\u4ee5\u4e0d\u586b', max_length=500, verbose_name='\u5185\u5bb9'),
        ),
    ]