from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django_filters.views import FilterView

from .models import Post, PostFilter


class PostList(FilterView):
    model = Post
    filterset_class = PostFilter
    queryset = Post.objects.filter(status='published').order_by('-created_at')
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
