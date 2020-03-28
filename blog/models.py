from django.db import models
from django.urls import reverse
import django_filters
from filer.fields.image import FilerImageField

from utils.models import UUIDModel, VersionedModel


POST_STATUSES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class Post(UUIDModel, VersionedModel):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    status = models.CharField(max_length=20, choices=POST_STATUSES, default=POST_STATUSES[0][0])
    content = models.TextField()
    photo = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name="post")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-post-detail', kwargs={'slug': self.slug})


class PostFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(lookup_type='contains')

    class Meta:
        model = Post
        fields = ['slug',]
