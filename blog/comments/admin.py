# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Comment

from blog.custom_site import cus_site


@admin.register(Comment, site=cus_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'nickname', 'status', 'created_time')


