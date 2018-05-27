# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.html import strip_tags

class Post(models.Model):
    STATUS_ITEMS = (
        (1, '上线'),
        (2, '草稿'),
        (3, '删除'),
    )
    TOP_ITEMS = (
        (0, '否'),
        (1, '是'),
    )

    title = models.CharField(max_length=100, verbose_name="标题")
    desc = models.CharField(max_length=255, blank=True, verbose_name="摘要")
    category = models.ForeignKey('Category', verbose_name="分类")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="标签")
    content = models.TextField(verbose_name="内容")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    weight = models.IntegerField(default=0, choices=TOP_ITEMS, verbose_name="置顶")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    pv = models.PositiveIntegerField(default=0, verbose_name="pv")
    uv = models.PositiveIntegerField(default=0, verbose_name="uv")

    class Meta:
        verbose_name = verbose_name_plural = "文章"

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def incr_pv(self):
        self.__class__._default_manager.filter(id=self.id).update(pv=F('pv') +1)

    def incr_uv(self):
        self.__class__._default_manager.filter(id=self.id).update(uv=F('uv') +1)

    def save(self, *args, **kwargs):
        if not self.desc.strip():
            self.desc = strip_tags(self.content)[:80]
        super(Post, self).save(*args, **kwargs)



class Category(models.Model):
    STATUS_ITEMS = (
        (1, '可用'),
        (2, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

    def __unicode(self):
        return self.name

class Tag(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=30, verbose_name="名称")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

