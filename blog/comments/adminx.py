# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Comment
import xadmin


class CommentAdmin(object):
    list_display = ('content', 'nickname', 'status', 'created_time')


xadmin.site.register(Comment, CommentAdmin)

