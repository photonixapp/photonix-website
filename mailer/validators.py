import re
from django.core.exceptions import ValidationError

from mailinglist.models import Subscription


def validate_template_variables(value):
    context = {
        'subscription': Subscription.objects.all()[0],
    }
    vars = re.findall(r'{{\s?(\S+)\s?}}', value)
    for var in vars:
        var_parts = var.split('.')
        if len(var_parts) < 2:
            raise ValidationError(u'\'{}\' variable is invalid'.format(var))
        try:
            getattr(context[var_parts[0]], var_parts[1])
        except KeyError:
            raise ValidationError(u'Found variable that is not in {}: \'{}\''.format(context.keys(), var_parts[0]))
        except AttributeError:
            raise ValidationError(u'\'{}\' object does not have a \'{}\' attribute'.format(var_parts[0], var_parts[1]))


def validate_no_html(value):
    tags = ['p', 'br', 'b', 'i', 'ul', 'li', 'hr', 'img', 'a', 'html', 'body', 'font']
    for tag in tags:
        if '<' + tag in value:
            raise ValidationError(u'Found HTML in field that should be plain text: <%s> tag' % tag)


def validate_html(value):
    tags = ['html', 'head', 'body']
    for tag in tags:
        if '<' + tag in value:
            raise ValidationError(u'Only HTML should be saved that can later be placed within a <body> tag. Found <%s> tag' % tag)
