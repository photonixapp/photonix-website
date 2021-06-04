
from django.db import models
from django.urls import reverse
from utils.models import UUIDModel, VersionedModel
from django.utils.text import slugify
import itertools


class Question(UUIDModel, VersionedModel):
    """Question model."""

    title = models.CharField(max_length=200, verbose_name="Question", help_text='Question asked')
    answer = models.TextField(verbose_name="Answer", null=True, blank=True, help_text='Answer to the question')
    slug = models.SlugField(null=True, blank=True, max_length=100)

    def __str__(self):
        """To show object."""
        return self.title

    def get_absolute_url(self):
        """Url for question detail page."""
        return reverse('question-detail', kwargs={'slug': self.slug})

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)[:max_length]
        for i in itertools.count(1):
            if not Question.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        """Slug field will save only once when object created not updated."""
        if not self.slug:
            self._generate_slug()
        super(Question, self).save(*args, **kwargs)
