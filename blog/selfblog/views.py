# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.test.utils import override_settings
from django.db import connection
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView

from .models import Post
from .models import Category
from .models import Tag
from config.models import Link, SideBar


PAGE_SIZE = 6


class CommonContextMixin(ContextMixin):

    def get_categories_context(self):
        categories = Category.objects.filter(status=1)
        cates = []
        nav_cate = []

        for c in categories:
            if c.is_nav:
                nav_cate.append(c)
            else:
                cates.append(c)

        return {'cates': cates, 'nav_cate': nav_cate}

    def get_tags_context(self):
        tags = Tag.objects.filter(status=1)
        return {'tags': tags}

    def get_sidebars_context(self):
        sidebar = SideBar.objects.filter(status=1).order_by('display_type')
        sidebars = {}
        for side in sidebar:
            sidebars[side.get_display_type_display()] = side

        return {'sidebars': sidebars}
    
    def get_recently_context(self):
        recently_post = Post.objects.filter(status=1).order_by('-created_time')[:10]
        return {'recently_post': recently_post}

    def get_links_context(self):
        links = Link.objects.filter(status=1).order_by('weight')
        return {'links': links}

    def get_common_context(self):
        context = {}
        context.update(self.get_links_context())
        context.update(self.get_recently_context())
        context.update(self.get_sidebars_context())
        context.update(self.get_tags_context())
        context.update(self.get_categories_context())
        return context

    def get_context_data(self, **kwargs):
        context = self.get_common_context()
        context.update(kwargs)
        context.update(self.extra_context)
        return super(CommonContextMixin, self).get_context_data(**context)


class BasePostView(ListView, CommonContextMixin):
    model = Post
    paginate_by = PAGE_SIZE
    context_object_name = "posts"
    ordering = ('-weight', '-created_time')
    template_name = "post/list.html"


class IndexView(BasePostView):
    extra_context = {'title': "Kylin的技术博客"}


class CategoryView(BasePostView):
    def get_queryset(self):
        queryset = super(CategoryView, self).get_queryset()
        
        category_id = self.kwargs.get('category_id')
        try:
            category = Category.objects.filter(status=1).get(id=int(category_id))
        except Category.DoesNotExist:
            raise Http404('category page not found')
        
        title = "{} | Kylin的技术博客".format(category.name)
        self.extra_context = {'title': title}
        
        queryset = queryset.filter(category_id=category.id)
        return queryset
   

class TagView(BasePostView):
    def get_queryset(self):
        queryset = super(TagView, self).get_queryset()
        
        tag_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.filter(status=1).get(id=int(tag_id))
        except Tag.DoesNotExist:
            raise Http404('tag page not found')
        
        title = "{} | Kylin的技术博客".format(tag.name)
        self.extra_context = {'title': title}
        
        queryset = queryset.filter(tags=tag.id)
        return queryset


class PostDetailView(DetailView, CommonContextMixin):
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = "post"
    template_name = "post/detail.html"

    def get_context_data(self, **kwargs):
        if self.object:
            post = self.object
            try:
                prev_post = Post.objects.filter(created_time__gt=post.created_time)[0]
            except IndexError:
                prev_post = None
            try:
                next_post = Post.objects.filter(created_time__lt=post.created_time)[0]
            except IndexError:
                next_post = None
            
            self.extra_context = {'prev_post': prev_post, 'next_post': next_post}
        
        return super(PostDetailView, self).get_context_data(**kwargs)


def test_m2m(request):
    #posts = Post.objects.get(id=1)
    #t = posts.tags.all()  # get m2m field 
    
    #posts = Post.objects.all()
    #for i in posts:
    #    print i.tags.all()
    #print connection.queries
    
    
    #posts = Post.objects.select_related('category').all()
    #for i in posts:
    #    print i.category.name
    #print connection.queries

#    cate = Category.objects.get(id=2)
#    posts = cate.post_set.all()
#    for i in posts:
#        print i.title
#    print connection.queries
    #p = Tag.objects.get(id=8)
    #p1 = Post.objects.filter(status=1, tags=p.id).prefetch_related('tags')
    #print p1
    #print connection.queries
    p = Tag.objects.get(id=8)
    p1 = p.post_set.all().prefetch_related('tags')
    print p1
    print connection.queries
    
    return HttpResponse('hello')


