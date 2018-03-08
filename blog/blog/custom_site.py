# coding:utf-8

from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite


class CustomSite(AdminSite):
    site_header = "博客管理后台"
    site_title = "首页"
    index_title = "博客管理"
    site_url = "http://www.baidu.com"


cus_site = CustomSite(name="cus_site")
