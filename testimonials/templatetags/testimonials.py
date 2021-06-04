
from django import template
from ..models import Testimonial
import random

register = template.Library()


@register.inclusion_tag('snippets/testimonials.html')
def random_tesimonals():
    """Implemented to show testimonial on any template."""
    try:
        random_items = random.sample(list(Testimonial.objects.all()), 3)
    except ValueError:
        random_items = list(Testimonial.objects.all()[:3])
    return {'testimonials_list': random_items}
