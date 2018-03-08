# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.core import urlresolvers

from .models import Post, Tag, Category
from blog.custom_site import cus_site
from .baseadmin import BaseOwnerAdmin


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    weight = forms.BooleanField(label="置顶", required=False)
    #other = forms.CharField(label="other", max_length=20)

    def clean_weight(self):
        is_top = self.cleaned_data['weight']
        return 1 if is_top else 0


'''
def set_on_top(obj):
    return '置顶' if obj.weight>0 else '没有置顶'

set_on_top.short_description = "是否置顶"
'''

class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  # 不如在ModelAdmin中做fileds
    actions_on_bottom = True  # 底部展示action
    actions_on_top = False       
    date_hierarchy = "created_time"  # 时间分类

    def set_on_top(self, obj):
        return True if obj.weight>0 else False
    set_on_top.boolean = True
    set_on_top.short_description = "是否置顶"


    def my_delete(self, obj):
        tmp_url = urlresolvers.reverse('cus_site:selfblog_post_delete', args=(obj.id,))
        return "<span><a href='{}'>删除</a></span>".format(tmp_url)
    my_delete.short_description = '删除'
    my_delete.allow_tags = True

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('title', 'set_on_top', 'owner', 'category', 'created_time', 'status', 'my_delete')
        else:
            return ('title', 'set_on_top', 'category', 'created_time', 'status', 'my_delete')
    list_display = ('category',) 
    list_filter = ('category__name', 'status', 'owner__username', 'tags')
    list_display_links = ('title',)
    list_editable = ('category',)


    # 修改页面配置
    #exclude = ('owner',)
    fields = ("title", 'desc', 'category', 'tags', 'content', ('status', 'weight'))
    #readonly_fields = ('title',)  # readonly
    
    #filter_horizontal = True  # manytomany字段过滤器界面
    #filter_vertical = True
    
    '''
    fieldsets = (
        ('基础', {
            'fields': ('title', 'desc', 'content', 'status')
            }),
        ('其他', {
            'classes': ('collapse',),
            'fields': ('category', 'tags', 'weight')
        }),
    )
    '''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(owner=request.user)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(owner=request.user)
        return super(PostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


cus_site.register(Post, PostAdmin)


class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('name', 'owner', 'status', 'created_time')
        else:
            return ('name', 'status', 'created_time')

cus_site.register(Tag, TagAdmin)


class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'is_nav', 'status', 'created_time')
    fields = ('name', 'is_nav', 'status')
    
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('name', 'is_nav', 'owner', 'status', 'created_time')
        else:
            return ('name', 'is_nav', 'status', 'created_time')

cus_site.register(Category, CategoryAdmin)
