from django.contrib import sitemaps
from django.urls import reverse

from faqs.models import Question


class QuestionSitemap(sitemaps.Sitemap):
    def items(self):
        items = [
            'faqs-list',
        ]
        items.extend(Question.objects.all().order_by('-created_at'))
        return items

    def priority(self, item):
        if type(item) == Question:
            return 0.5
        return 0.7

    def lastmod(self, item):
        if type(item) == Question:
            return item.created_at
        if not Question.objects.all().order_by('-created_at'):
            return None
        return Question.objects.all().order_by('-created_at')[0].created_at

    def changefreq(self, item):
        if type(item) == Question:
            return 'monthly'
        return 'weekly'

    def location(self, item):
        if type(item) == Question:
            return reverse('faqs-detail', kwargs={'slug': item.slug})
        return reverse(item)
