from random import random
import re
from time import sleep

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from matomo_monorail.utils import get_client_ip

from utils.mattermost import notify_mattermost

from .models import Subscription


@csrf_exempt
def signup(request):
    email = request.POST.get('email')
    source = request.POST.get('source', '')
    medium = request.POST.get('medium', '')
    campaign = request.POST.get('campaign', '')

    landing_page = ''
    referer = request.META.get('HTTP_REFERER', '')
    regex = r'\/landing\/(\S+)\/'
    try:
        landing_page = re.search(regex, referer).group(1)
    except:
        pass

    if not email:
        raise TypeError('Invalid email address')

    ip = get_client_ip(request)
    language = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0]

    try:
        subscription = Subscription(email=email, ip=ip, language=language, source=source, medium=medium, campaign=campaign, landing_page=landing_page)
        subscription.save()
        total_subscribers = Subscription.objects.count()

        notify_mattermost(
            text='🎉 New Photonix mailing list subscription',
            attachments=[{
                'title': 'User details',
                "color": "#36a64f",
                'fields': [
                    {'title': 'Email', 'value': email, 'short': True},
                    {'title': 'Total subscribers', 'value': f"{total_subscribers:,}", 'short': True},
                ],
            }]
        )

    except IntegrityError:
        pass

    sleep((random() / 2) + 0.5)  # Mitigate against timing-based attack of determining if email address is already in DB

    context = {
        'email': email
    }
    return HttpResponseRedirect('/mailinglist/confirmation')


def confirmation(request):
    context = {}
    return render(request, 'mailinglist/confirmation.html', context)