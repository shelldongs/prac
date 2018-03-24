"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .custom_site import cus_site
from selfblog.views import PostDetailView, IndexView, CategoryView, TagView, SearchView,test, comment


urlpatterns = [
    url(r"^comment$", comment),
    url(r"^test$", test),
    url(r'^self/admin/', admin.site.urls),
    url(r'^self/blog_admin/', cus_site.urls),
    url(r'^blog/', include('selfblog.urls')),
    url(r'^search$', SearchView.as_view(), name="search_post"),
    url(r'^(?P<author_name>\w+)$', IndexView.as_view(), name="post_list"),
    url(r'^(?P<author_name>\w+)/post/(?P<post_id>\d+)$', PostDetailView.as_view(), name="post_detail"),
    url(r'^(?P<author_name>\w+)/category/(?P<category_id>\d+)$', CategoryView.as_view(), name="category_post_list"),
    url(r'^(?P<author_name>\w+)/tag/(?P<tag_id>\d+)$', TagView.as_view(), name="tag_post_list"),
    
]





