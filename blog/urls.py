from django.conf.urls import include, url
from django.urls import path

from .feeds import BlogFeed
from .views import PostList, PostDetail


urlpatterns = [
    path('', PostList.as_view(), name='blog-post-list'),
    path('feed/', BlogFeed(), name='blog-post-feed'),
    path('<slug:slug>/', PostDetail.as_view(), name='blog-post-detail'),
]
