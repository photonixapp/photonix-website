from django.contrib.syndication.views import Feed
import markdown

from .models import Post


class BlogFeed(Feed):
    title = "Photonix Blog Feed"
    link = "/blog/"
    description = "Lastest updates about development of Photonix"

    def items(self):
        return Post.objects.order_by('-created_at')[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown.Markdown().convert(item.content)
