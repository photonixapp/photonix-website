from html.parser import HTMLParser
from io import StringIO
import re

from django import template
from django.template.defaultfilters import stringfilter

from ..utils import gallery_dir, gallery_image


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

    value = ''.join(contentElements)
    contentElements = []
    for item in re.split('(\[!gallery-image [\S]+\])', value):
        if item.startswith('[!gallery-image '):
            matches = re.match(r'\[!gallery-image ([\S]+)\]', item)
            path = matches.group(1)
            contentElements.append(gallery_image(path))
        else:
            contentElements.append(item)

    return ''.join(contentElements)


# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


@register.filter(is_safe=True)
@stringfilter
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
