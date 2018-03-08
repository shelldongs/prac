# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.test.utils import override_settings
from django.db import connection

from .models import Post
from .models import Category
from .models import Tag


def post_list(request, category_id=None, tag_id=None):
    queryset = Post.objects.all()
    
    if category_id:
        queryset = queryset.filter(category_id=int(category_id))
    
    if tag_id:
        try:
            tag = Tag.objects.get(id=int(tag_id))
        except Tag.DoesNotExist:
            raise Http404('page not found')
        queryset = tag.post_set.all()
    
    context_data = {
        'posts': queryset.order_by('-weight', '-created_time')
    }
    
    return render(request, 'post/list.html', context=context_data)


def post_detail(request, post_id):
    try:
        queryset = Post.objects.get(id=int(post_id))
    except Post.DoesNotExist:
        raise Http404("page not found")
    
    context_data = {
        'post': queryset
    }
    return render(request, 'post/detail.html', context=context_data)


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
    p = Post.objects.all()
    p1 = p[:5]
    print p1
    p2 = p[5:10]
    print p2
    print connection.queries
    
    return HttpResponse('hello')
