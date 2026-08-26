import markdown
from django.contrib.syndication.views import Feed

from .models import Post


class BlogFeed(Feed):
    title = 'Photonix Blog Feed'
    link = '/blog/'
    description = 'Lastest updates about development of Photonix'

    def items(self):
        return Post.objects.filter(status='published').order_by('-created_at')[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown.Markdown().convert(item.content)
