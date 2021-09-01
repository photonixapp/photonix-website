from random import random
import re
from time import sleep

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from matomo_monorail.utils import get_client_ip
import requests

from .models import Subscription, List, ListUnsubscribes
from .forms import UnsubscribeForm


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

    return HttpResponseRedirect('/mailinglist/confirmation/')


def preferences(request):
    context = {}
    email = request.GET.get('email', '')
    token = request.GET.get('token', '')
    context['email'] = email
    context['token'] = token

    if request.method == 'POST':
        print(request.POST)
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            subscription = Subscription.objects.get(email=email)
            subscription.unsubscribed_from_all_lists = form.cleaned_data['unsubscribe_all']
            ListUnsubscribes.objects.filter(subscription=subscription).delete()
            print(form.cleaned_data)
            for list_name in form.cleaned_data['unsubscribes']:
                print(list_name)
                list = List.objects.get(name=list_name)
                lu = ListUnsubscribes(list=list, subscription=subscription)
                lu.save()
            subscription.save()
            return HttpResponseRedirect(reverse('preferences-updated'))
        context['form'] = form
    else:
        context['form'] = UnsubscribeForm()
    return render(request, 'mailinglist/preferences.html', context)
