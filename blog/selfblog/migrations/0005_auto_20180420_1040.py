# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-20 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfblog', '0004_auto_20180420_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(1, '\u4e0a\u7ebf'), (2, '\u8349\u7a3f'), (3, '\u5220\u9664')], default=1, verbose_name='\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='post',
            name='weight',
            field=models.IntegerField(choices=[(0, '\u5426'), (1, '\u662f')], default=0, verbose_name='\u7f6e\u9876'),
        ),
    ]
