# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    title = models.CharField(max_length=50, verbose_name="网站名")
    href = models.URLField(verbose_name="链接")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.IntegerField(default=1, verbose_name="权重")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"


class SideBar(models.Model):
    STATUS_ITEMS = (
        (1, '展示'),
        (2, '下线'),
    )
    SIDE_TYPE = (
        (1, 'HTML'),
        (2, '最新文章'),
        (3, '最热文章'),
        (4, '最新评论'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.IntegerField(default=1, choices=SIDE_TYPE, 
                                       verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, 
                               verbose_name="内容", help_text="非HTML类型，可以不填")
    owner = models.ForeignKey(User, verbose_name="作者")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"


