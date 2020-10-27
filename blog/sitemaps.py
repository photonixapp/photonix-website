from django.contrib import sitemaps
from django.urls import reverse

from .models import Post


class BlogSitemap(sitemaps.Sitemap):
    def items(self):
        items = [
            'blog-post-list',
        ]
        items.extend(Post.objects.filter(status='published').order_by('-created_at'))
        return items

    def priority(self, item):
        if type(item) == Post:
            return 0.5
        return 0.7

    def lastmod(self, item):
        if type(item) == Post:
            return item.created_at
        return Post.objects.filter(status='published').order_by('-created_at')[0].created_at

    def changefreq(self, item):
        if type(item) == Post:
            return 'monthly'
        return 'weekly'

    def location(self, item):
        if type(item) == Post:
            return reverse('blog-post-detail', kwargs={'slug': item.slug})
        return reverse(item)
