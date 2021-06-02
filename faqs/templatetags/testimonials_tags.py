
from django import template
from django.template.loader import get_template
from faqs.models import Testimonial
import random

register = template.Library()


@register.inclusion_tag('snippets/testimonials_reviews.html')
def get_random_tesimonals():
    """Implemented to show testimonial on any template."""
    random_items = random.sample(list(Testimonial.objects.all()), 3)
    return {'testimonials_list': random_items}

