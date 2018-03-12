# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Link, SideBar

from blog.custom_site import cus_site


@admin.register(Link, site=cus_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')



@admin.register(SideBar, site=cus_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'created_time')


