# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from django import forms
from django.contrib import admin
from django.core import urlresolvers
from django.urls import reverse

from .models import Post, Tag, Category
from blog.custom_site import cus_site
from blog.adminx import BaseOwnerAdmin
import xadmin
from xadmin.layout import Fieldset, Row
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class TagTextInput(forms.TextInput):
    def format_value(self, value):
        if value:
            values = value.values_list('name', flat=True)
            value = [v for v in values]
            return ','.join(value)



class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'style':'width:830px;'}), label='摘要', required=False)
    #other = forms.CharField(label="other", max_length=20)
    
    category = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        widget = autocomplete.ModelSelect2(url='category-autocomplete'),
        label = "分类",
    )

#    tags = forms.ModelMultipleChoiceField(
#        queryset = Tag.objects.all(),
#        widget = autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
#        label = "Tag",
#    )

    #tags = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), max_length=100, label="标签", help_text=",分割标签,最多十个标签")
    tags = forms.CharField(max_length=100, widget=TagTextInput(attrs={'style': 'width:830px;'}), label="标签",  help_text=",分割标签,最多十个标签")
    content = forms.CharField(widget=CKEditorUploadingWidget(), label="正文")


    def clean_tags(self):
        tags = self.cleaned_data['tags'].lower().strip().split(',')
        return tags

'''
def set_on_top(obj):
    return '置顶' if obj.weight>0 else '没有置顶'

set_on_top.short_description = "是否置顶"
'''


class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  
    actions_on_bottom = True  # 底部展示action
    actions_on_top = False       
    date_hierarchy = "created_time"  # 时间分类

    def set_on_top(self, obj):
        return True if obj.weight>0 else False
    set_on_top.boolean = True
    set_on_top.short_description = "是否置顶"

    def save_models(self):
        tags = self.form_obj.cleaned_data['tags']
        ts = []
        for t in tags:
            tag, created = Tag.objects.get_or_create(name=t, owner=self.request.user)
            ts.append(tag)
        self.form_obj.cleaned_data['tags'] = ts
        return super(PostAdmin, self).save_models()

    def my_delete(self, obj):
        #tmp_url = urlresolvers.reverse('cus_site:selfblog_post_delete', args=(obj.id,))
        tmp_url = reverse('xadmin:selfblog_post_delete', args=(obj.id,))
        h = "<span><a href='{}'>删除</a></span>".format(tmp_url)
        from django.utils.safestring import mark_safe
        return mark_safe(h)
    my_delete.short_description = '删除'
    #my_delete.allow_tags = True

    def change_post(self, obj):
        tmp_url = reverse('xadmin:selfblog_post_change', args=(obj.id,))
        h = "<span><a href='{}'>编辑</a></span>".format(tmp_url)
        from django.utils.safestring import mark_safe
        return mark_safe(h)
    change_post.short_description = '编辑'

    def view_post(self, obj):
        tmp_url = reverse('post_detail', args=(self.request.user, obj.id,))
        h = "<span><a target='view_window' href='{}'>{}</a></span>".format(tmp_url, obj.title)
        from django.utils.safestring import mark_safe
        return mark_safe(h)
    view_post.short_description = '浏览'

#    def get_list_display(self, request):  # 此处也应该调用父类
#        if request.user.is_superuser:
#            return ('title', 'set_on_top', 'owner', 'category', 
#                    'created_time', 'status', 'my_delete', 'pv', 'uv')
#        else:
#            return ('title', 'set_on_top', 'category', 'created_time', 'status', 'my_delete', 'pv', 'uv')


# xadmin 版本 
    def get_list_display(self):
        list_dis = super(PostAdmin, self).get_list_display()
        #print self.base_list_display  # 由上面得到，一般是list_display中字段 
        if self.request.user.is_superuser:
            list_dis.append('set_on_top', 'owner')
        else:
            list_dis.append('set_on_top')
        return list_dis


    list_display = ('view_post', 'change_post', 'pv', 'uv', 'status', 'my_delete', 'created_time') 
    list_filter = ('category__name', 'status', 'owner__username', 'tags')
    #list_display_links = ('title',)
    #list_editable = ('category',)  # 会造成大量外键查询


    # 修改页面配置
    #fields = ("title", 'desc', 'category', 'tags', 'content', ('status', 'weight'))

    # 编辑页面
    form_layout = (
        Fieldset(
            '文章编辑',
            'title',
            'content',
            'desc',
            'category',
            'tags',
            'status', 'weight',
        )
    )

    # 不出现在编辑页面
    exclude = ('owner', 'pv', 'uv')

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

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == 'category':
#            kwargs['queryset'] = Category.objects.filter(owner=request.user)
#        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
#    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        if db_field.name == 'tags':
#            kwargs['queryset'] = Tag.objects.filter(owner=request.user)
#        return super(PostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


xadmin.site.register(Post, PostAdmin)


class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')

    form_layout = (
        Fieldset(
            '标签',
            'name',
            'status',
        )
    )
    exclude = ('owner',)
#    def get_list_display(self, request):
#        if request.user.is_superuser:
#            return ('name', 'owner', 'status', 'created_time')
#        else:
#            return ('name', 'status', 'created_time')


xadmin.site.register(Tag, TagAdmin)


class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'is_nav', 'status', 'created_time')
    
    form_layout = (
        Fieldset(
            '分类',
            'name',
            'is_nav',
            'status',
        )
    )

    exclude = ('owner',)
#    def get_list_display(self, request):
#        if request.user.is_superuser:
#            return ('name', 'is_nav', 'owner', 'status', 'created_time')
#        else:
#            return ('name', 'is_nav', 'status', 'created_time')


xadmin.site.register(Category, CategoryAdmin)
