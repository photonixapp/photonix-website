from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# @register.simple_tag(takes_context=True)
@register.inclusion_tag('mailinglist/mailinglist_tracking_fields.html', takes_context=True)
def mailinglist_tracking_fields(context):
    request = context['request']
    field_names = ['source', 'medium', 'campaign']
    fields = {}
    for field in field_names:
        val = request.GET.get(field)
        if not val:
            val = request.GET.get(f'pk_{field}')
        if val:
            fields[field] = val
    return {'fields': fields}
