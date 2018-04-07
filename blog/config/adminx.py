# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Link, SideBar
import xadmin
from django import forms
from blog.adminx import BaseOwnerAdmin

class SideBarForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='html', required=False)


class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    exclude = ['owner']


xadmin.site.register(Link, LinkAdmin)


class SideBarAdmin(BaseOwnerAdmin):
    form = SideBarForm
    list_display = ('title', 'display_type', 'created_time')
    exclude = ['owner']
    

xadmin.site.register(SideBar, SideBarAdmin)

