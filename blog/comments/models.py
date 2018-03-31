# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from selfblog.models import Post


class Comment(models.Model):
    STATUS_ITEMS = (
        (1, '可用'),
        (2, '删除'),
    )
    target = models.CharField(max_length=100, verbose_name="target")
    content = models.CharField(max_length=200, verbose_name="内容")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    pid = models.ForeignKey('Comment', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"


