from django.http import HttpResponse
from matomo_monorail.utils import get_client_ip


def ip(request):
    content = f'{get_client_ip(request)}, is_secure() = {request.is_secure()}'
    return HttpResponse(content, content_type='text/plain')
