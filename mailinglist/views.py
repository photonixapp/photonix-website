from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import Subscription

@csrf_exempt
def signup(request):
    email = request.POST.get('email')

    if not email:
        return
    
    Subscription(email=email).save()

    context = {
        'email': email
    }
    return HttpResponseRedirect('/mailinglist/confirmation')


def confirmation(request):
    context = {}
    return render(request, 'mailinglist/confirmation.html', context)