from django import template
import time
import os
import random


register = template.Library()


@register.simple_tag
def version_date():
    if os.environ.get('ENV', 'dev') in ['stg', 'prd']:
        return time.strftime('%Y%m%d%H%M', time.gmtime(os.path.getmtime('.git')))
    return random.random()
