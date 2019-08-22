from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# import requests

from .models import Subscription


@csrf_exempt
def signup(request):
    email = request.POST.get('email')

    if not email:
        return
    
    Subscription(email=email).save()

    requests.post('https://skylark.epixstudios.co.uk/webhook/', params={
        'title': "New Photonix mailing list subscription",
        'body': 'Domain: {}  Total: {}'.format(email.split('@')[-1], Subscription.objects.count()),
        'color': '#12b9de',
    })

    context = {
        'email': email
    }
    return HttpResponseRedirect('/mailinglist/confirmation')


def confirmation(request):
    context = {}
    return render(request, 'mailinglist/confirmation.html', context)