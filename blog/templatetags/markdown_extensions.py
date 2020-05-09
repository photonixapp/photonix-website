import re

from django import template
from django.template.defaultfilters import stringfilter

from ..utils import gallery_dir


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def format_extensions(value):
    contentElements = []
    for item in re.split('(\[!gallery-dir [\d]+ [\S]+\])', value):
        if item.startswith('[!gallery-dir '):
            matches = re.match(r'\[!gallery-dir ([\d]+) ([\S]+)\]', item)
            cols = matches.group(1)
            path = matches.group(2)
            contentElements.append(gallery_dir(cols, path))
        else:
            contentElements.append(item)

    return ''.join(contentElements)
