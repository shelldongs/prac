# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pdb

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.test.utils import override_settings
from django.db import connection
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView
from django.core.cache import caches
from django.core.cache import cache
from django.contrib.auth.models import User
import hashlib
from django.utils.html import escape


from .models import Post
from .models import Category
from .models import Tag
from config.models import Link, SideBar 
from comments.models import Comment


PAGE_SIZE = 10 


class CommonContextMixin(ContextMixin):
    def get_categories_context(self):
        categories = Category.objects.filter(owner_id=self.owner.id, status=1)
        cates = []
        nav_cate = []

        for c in categories:
            if c.is_nav:
                nav_cate.append(c)
            else:
                cates.append(c)

        return {'cates': cates, 'nav_cate': nav_cate}

    def get_tags_context(self):
        tags = Tag.objects.filter(owner_id=self.owner.id, status=1)
        return {'tags': tags}

    def get_sidebars_context(self):
        sidebar = SideBar.objects.filter(owner_id=self.owner.id, status=1).order_by('display_type')
        sidebars = {}
        for side in sidebar:
            sidebars[side.get_display_type_display()] = side

        return {'sidebars': sidebars}
    
    def get_recently_context(self):
        recently_post = Post.objects.filter(owner_id=self.owner.id, status=1).order_by('-created_time')[:10]
        return {'recently_post': recently_post}

    def get_links_context(self):
        links = Link.objects.filter(owner_id=self.owner.id, status=1).order_by('weight')
        return {'links': links}

    def get_hot_post(self):
        hot_post = Post.objects.filter(owner_id=self.owner.id, status=1).order_by('-pv')[:10]
        return {'hot_post': hot_post}

    def get_common_context(self):
        context = {"username": self.username}
        context.update(self.get_links_context())
        context.update(self.get_recently_context())
        context.update(self.get_sidebars_context())
        context.update(self.get_tags_context())
        context.update(self.get_categories_context())
        context.update(self.get_hot_post())
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

    def get_queryset(self):
        author_name = self.kwargs.get('author_name') or self.request.GET.get('username')
        user = User.objects.filter(username__iexact=author_name)
        try:
            owner = user.get()
        except:
            raise Http404('bad username')
        self.owner = owner
        self.username = author_name.lower()
        queryset = super(BasePostView, self).get_queryset()
        return queryset.filter(owner_id=self.owner.id)

    def get_context_data(self, **kwargs):
        context = super(BasePostView, self).get_context_data(**kwargs)
        for post in context['posts']:
            postpv_count_key = "count:Post:pv:{}".format(post.id)
            postuv_count_key = "count:Post:uv:{}".format(post.id)

            pv = cache.get(postpv_count_key, None)
            if pv:
                post.pv = pv
            uv = cache.get(postuv_count_key, None)
            if uv:
                post.uv = uv
        return context
        
class IndexView(BasePostView):
    extra_context = {'title': "Kylin的技术博客"}


class SearchView(BasePostView):
    extra_context = {'title': "Search | Kylin的技术博客"}

    def get_queryset(self):
        query_str = self.request.GET.get('q')
        self.q = query_str
        queryset = super(SearchView, self).get_queryset()
        if query_str:
            queryset = queryset.filter(title__icontains=query_str)
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        if self.q:
            context = {'q': self.q}
        context.update(kwargs)
        return super(SearchView, self).get_context_data(**context)


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

    def get_queryset(self):
        author_name = self.kwargs.get('author_name')
        user = User.objects.filter(username__iexact=author_name)
        try:
            owner = user.get()
        except:
            raise Http404('bad username')
        self.owner = owner
        self.username = author_name.lower()
        queryset = super(PostDetailView, self).get_queryset()
        return queryset.filter(owner_id=self.owner.id)
    
    def get_context_data(self, **kwargs):
        post = self.object
        try:
            prev_post = Post.objects.filter(owner_id=self.owner.id, created_time__gt=post.created_time)[0]
        except IndexError:
            prev_post = None
        try:
            next_post = Post.objects.filter(owner_id=self.owner.id, created_time__lt=post.created_time)[0]
        except IndexError:
            next_post = None
       
        p = self.request.path
        com = Comment.objects.filter(target=p).order_by('pid', '-created_time')
        kwargs.update({"com": com})

        self.extra_context = {'prev_post': prev_post, 'next_post': next_post}
        self.incr_pvuv()
        self.get_pvuv()
        return super(PostDetailView, self).get_context_data(**kwargs)
   
    def get_pvuv(self):
        postpv_count_key = "count:Post:pv:{}".format(self.object.id)
        postuv_count_key = "count:Post:uv:{}".format(self.object.id)

        pv = cache.get(postpv_count_key, None)
        if pv:
            self.object.pv = pv
        uv = cache.get(postuv_count_key, None)
        if uv:
            self.object.uv = uv

    def incr_pvuv(self):
        sessionid = self.request.COOKIES.get('_uid', None)
        if not sessionid:
            agent = self.request.META['HTTP_USER_AGENT']
            addr = self.request.META['REMOTE_ADDR']
            salt = "4325u9034u2569@#()*Q&($%)"
            key_str = "{}:{}:{}".format(agent, addr, salt)
            key = hashlib.md5(key_str).hexdigest()  # 没有区分无痕浏览器
            sessionid = key
        
        self._uid = sessionid

        postpv_flag_key = "{1}:flag:Post:pv:{0}".format(self.object.id, sessionid)
        postpv_count_key = "count:Post:pv:{}".format(self.object.id)
        postuv_flag_key = "{1}:flag:Post:uv:{0}".format(self.object.id, sessionid)
        postuv_count_key = "count:Post:uv:{}".format(self.object.id)

        post = self.model.objects.get(id=self.object.id)

        if not cache.get(postpv_count_key, None):
            cache.set(postpv_count_key, post.pv, timeout=None)
        if not cache.get(postuv_count_key, None):
            cache.set(postuv_count_key, post.uv, timeout=None)
        
        if not cache.get(postpv_flag_key, None):
            cache.set(postpv_flag_key, 1, 5*60)
            cache.incr(postpv_count_key)
        if not cache.get(postuv_flag_key, None):
            cache.set(postuv_flag_key, 1, 8*60*60)
            cache.incr(postuv_count_key)
        
    def get(self, request, *args, **kwargs):
        ret =  super(PostDetailView, self).get(request, *args, **kwargs)
        ret.set_cookie('_uid', self._uid)
        return ret


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


from django.views.decorators.csrf import csrf_exempt
import datetime

def comment(request):
    pid = request.POST.get("pid")
    target = request.POST.get("target")
    txt = request.POST.get("txt")
    txt = escape(txt)
    if pid == "0":
        com = Comment.objects.create(content=txt, nickname='nobody', target=target)
    else:
        c = Comment.objects.get(id=pid)
        com = Comment.objects.create(content=txt, nickname='nobody', target=target, pid=c)
    
    return JsonResponse({'id': com.id, 'txt': txt, 'created_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})



def test(request):
    return render(request, "post/test.html", context={})
