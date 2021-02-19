from random import random
import re
from time import sleep

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from matomo_monorail.utils import get_client_ip
import requests

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

        requests.post('https://skylark.epixstudios.co.uk/webhook/', params={
            'title': "New Photonix mailing list subscription",
            'body': 'Total: {} | {} | {}'.format(Subscription.objects.count(), email.split('@')[-1], subscription.country),
            'color': '#12b9de',
            'icon': 'https://photonix.org/static/images/favicon.png',
        })

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