import os
from datetime import datetime

from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['index', 'privacy-policy']

    def priority(self, item):
        priorities = {
            'index': 1.0,
        }
        return priorities.get(item, 0.5)

    def lastmod(self, item):
        return datetime.fromtimestamp(os.path.getmtime('/srv/.git'))

    def location(self, item):
        return reverse(item)