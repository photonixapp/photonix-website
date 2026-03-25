from django.urls import path

from .feeds import BlogFeed
from .views import PostDetail, PostList

urlpatterns = [
    path('', PostList.as_view(), name='blog-post-list'),
    path('feed/', BlogFeed(), name='blog-post-feed'),
    path('<slug:slug>/', PostDetail.as_view(), name='blog-post-detail'),
]
