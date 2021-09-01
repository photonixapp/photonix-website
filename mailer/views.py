import json

from django.contrib.admin.helpers import AdminForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.template import Context, Template
from django.views.decorators.cache import never_cache

from mailinglist.models import Subscription
from .forms import MassSendForm
from .models import Template as MailerTemplate, Job, Tracker
from .tasks import start_job


@staff_member_required
def mass_send(request):
    try:
        default_template = MailerTemplate.objects.order_by('-updated_at')[0]
        default_data = {'recipients': request.GET['recipient_ids'], 'template': default_template.id}
    except IndexError:
        default_data = {}
    num_recipients = len(request.GET['recipient_ids'].split(','))

    if request.method == 'POST':
        default_data.update(request.POST)
        form = MassSendForm(default_data)
        if form.is_valid():
            template_id = int(request.POST['template'])
            template = MailerTemplate.objects.get(id=template_id)
            recipient_ids = request.POST['recipients'].split(',')
            recipients = Subscription.objects.filter(id__in=recipient_ids)
            job = Job(status='new', template=template)
            job.save()
            job.recipients.set(recipients)
            job.save()
            start_job.delay(job.id)
            return HttpResponseRedirect('/mailer/mass-send/progress/?job_id={}'.format(job.id))
    else:
        form = MassSendForm(default_data)

    fieldsets = [(None, {'fields': list(form.base_fields)})]
    adminform = AdminForm(form, fieldsets, {})

    context = {
        'title': 'Mailer Mass Send',
        'save_on_top': False,
        'add': False,
        'adminform': adminform,
        'num_recipients': num_recipients,
        'opts': MailerTemplate._meta,
    }
    return render(request, 'mailer/mass_send.html', context)


@staff_member_required
def mass_send_preview(request):
    try:
        template = MailerTemplate.objects.get(id=int(request.GET['template_id']))
        body = '<strong>' + template.subject + '</strong><hr/>'
        if template.content_html:
            body += template.content_html
        else:
            body += '<pre>' + template.content_plain + '</pre>'

        if 'subscription_id' in request.GET:
            subscription = Subscription.objects.get(id=int(request.GET['subscription_id']))
        else:
            subscription = Subscription.objects.order_by('?')[0]
        context = Context({
            'subscription': subscription,
        })

        template = Template(body)
        return HttpResponse(template.render(context))
    except ValueError:
        return HttpResponse('', status=400)


@never_cache
@staff_member_required
def mass_send_progress(request):
    job = Job.objects.get(id=int(request.GET['job_id']))
    context = {
        'title': 'Mailer Mass Send',
        'id': job.id,
        'status': job.status,
        'num_recipients': job.num_recipients,
        'num_messages_sent': job.num_messages_sent,
        'percent_complete': job.percent_complete,
    }
    if request.GET.get('is_ajax'):
        return HttpResponse(json.dumps(context), content_type='application/json')
    else:
        context['job'] = job
        return render(request, 'mailer/mass_send_progress.html', context)


def tracking_redirect(request, tracker_id, recipient_id, salt, signature):
    '''
    https://courchevel-1650.com/mailer/r/1/1/G8cK5N/pfk-6r/
    '''
    tracker = Tracker.objects.get(id=int(tracker_id))
    tracker.track_event(recipient_id, salt, signature)

    if tracker.type in ['link', 'image']:
        if tracker.url:
            return HttpResponseRedirect(tracker.url)
    elif tracker.type == 'pixel':
        image_data = 'GIF87a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        response = HttpResponse(content_type='image/gif')
        response.write(image_data)
        return response
    return HttpResponseNotFound()
