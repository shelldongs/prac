# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import connection
from django.test.utils import override_settings

from .models import Category


class BlogTest(TestCase):
    def setUp(self):
        self.test_filter()
        user = User.objects.create_user("dongbala8", "555@qq.com", "1234")
        for i in range(10):
            category_name = "cate_%s" %i
            Category.objects.create(name=category_name, owner=user)

    @override_settings(DEBUG=True)
    def test_filter(self):
        cs = Category.objects.all().iterator()
        for i in cs:
            print i
        print connection.queries



