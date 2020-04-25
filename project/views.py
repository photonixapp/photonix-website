from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from matomo_monorail.utils import get_client_ip


def ip(request):
    content = f'{get_client_ip(request)}, is_secure() = {request.is_secure()}'
    return HttpResponse(content, content_type='text/plain')


def landing(request, slug):
    context = {}
    try:
        return render(request, f'landing/{slug}.html', context)
    except TemplateDoesNotExist:
        raise Http404
