import os
import random
import time

from django import template

register = template.Library()


@register.simple_tag
def version_date():
    if os.environ.get('ENV', 'dev') in ['stg', 'prd']:
        return time.strftime('%Y%m%d%H%M', time.gmtime(os.path.getmtime('.git')))
    return random.random()
