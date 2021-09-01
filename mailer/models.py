import base64
from datetime import datetime
import re
from smtplib import SMTPException
from time import sleep

from django.core.mail import send_mail
from django.db import models
from django.template import Context, Template as DjangoTemplate
from django.template.loader import get_template
from django.utils import crypto, timezone

from mailinglist.models import Subscription
from utils.models import UUIDModel, VersionedModel
from .tasks import send_message
from .validators import validate_template_variables, validate_no_html, validate_html


TEMPLATE_TYPE = (
    ('marketing_email', 'Marketing email'),
    ('transactional_email', 'Transactional email'),
)


class Template(VersionedModel):
    '''
    Template can be for mass email marketing shot, a template email relating to
    a booking (which might not nescessarily be sent through the job runner), or
    potentially in the future a booking customer update SMS.
    '''
    type = models.CharField(max_length=20, choices=TEMPLATE_TYPE)
    subject = models.CharField(max_length=100, validators=[validate_template_variables, validate_no_html])
    content_plain = models.TextField(blank=True, validators=[validate_template_variables, validate_no_html])
    content_html = models.TextField(blank=True, verbose_name='content HTML', validators=[validate_template_variables, validate_html])

    def __str__(self):
        return self.subject


MESSAGE_STATUSES = (
    ('new', 'New'),
    ('running', 'Running'),
    ('complete', 'Complete'),
    ('failed', 'Failed'),
)


class Job(VersionedModel):
    '''
    When a template is to sent out to a batch of recipients, one of these Jobs
    is created. This then starts up parallel processes to send each of the
    emails - these are represented in the Message model.
    '''
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    recipients = models.ManyToManyField(Subscription)
    status = models.CharField(max_length=8, choices=MESSAGE_STATUSES)
    time_taken_ms = models.PositiveIntegerField(null=True)

    current_tasks = []

    def __str__(self):
        return u'[{}] {}, {} recipients'.format(self.status.upper(), self.template, self.num_recipients)

    @property
    def num_recipients(self):
        return self.recipients.count()

    @property
    def num_messages_sent(self):
        return Message.objects.filter(job=self, status__in=['complete', 'failed']).count()

    @property
    def num_messages_remaining(self):
        return Message.objects.filter(job=self, status__in=['new', 'running']).count()

    @property
    def percent_complete(self):
        if not self.num_messages_sent or not self.num_recipients:
            return 0
        return int((float(self.num_messages_sent) / self.num_recipients) * 100)

    def start(self):
        start = datetime.now()
        if self.status != 'new':
            raise AttributeError('Job {} has already been run'.format(self.id))
        self.status = 'running'
        self.save()

        for i, recipient in enumerate(self.recipients.all()):
            tracking_pixel = Tracker.objects.add_tracker(self.id, 'pixel', recipient.id)
            context = {'customer': recipient, 'tracking_pixel': tracking_pixel}

            # Subject can have template variables
            subject = DjangoTemplate(self.template.subject).render(Context(context))

            # Plain text email template rendering and adding tracking redirects
            content = self.template.content_plain
            links = set(re.findall(r'https?:\/\/\S+', content))
            for link in links:
                tracking_url = Tracker.objects.add_tracker(self.id, 'link', recipient.id, link)
                content = content.replace(link, tracking_url)
            context['body'] = DjangoTemplate(content).render(Context(context))
            content_plain = get_template('mailer/email.txt').render(context)

            # HTML email template rendering and adding tracking redirects
            content = self.template.content_html
            links = set(re.findall(r'(href|src)\=(["\'])(https?:\/\/\S+)["\']', content))
            for link in links:
                tracking_url = Tracker.objects.add_tracker(self.id, 'link', recipient.id, link[2])
                content = content.replace('{}={}{}{}'.format(link[0], link[1], link[2], link[1]), '{}={}{}{}'.format(link[0], link[1], tracking_url, link[1]))
            context['body'] = DjangoTemplate(content).render(Context(context))
            content_html = get_template('mailer/email.html').render(context)

            message = Message(
                recipient=recipient,
                job=self,
                status='new',
                subject=subject,
                content_plain=content_plain,
                content_html=content_html
            )
            message.save()
            send_message.delay(message.id)

            if i % 10 == 0:
                self.tasks_are_completed()

        while not self.tasks_are_completed():
            sleep(0.2)

        self.status = 'complete'
        self.time_taken_ms = int((datetime.now() - start).total_seconds() * 1000)
        self.save()

    def tasks_are_completed(self):
        for task in self.current_tasks:
            if task.state.ready():
                self.current_tasks.remove(task)
        if len(self.current_tasks):
            return False
        if self.num_messages_remaining:
            return False
        return True

    def recipients_read(self):
        return TrackerEvent.objects.filter(tracker__job_id=self.id).values_list('recipient_id', flat=True).distinct()

    def num_recipients_read(self):
        return self.recipients_read().count()


class Message(VersionedModel):
    '''
    A Message record is stored for each attempt to send to a recipient. These
    are either created by Job if there are multiple recipients or by other
    pieces of code such as in booking management.
    '''
    recipient = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    job = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True)  # Doesn't need to be set if it's a single email
    subject = models.CharField(max_length=100)
    content_plain = models.TextField(blank=True)  # If Message is not part of a Job then there must be content here
    content_html = models.TextField(blank=True)
    status = models.CharField(max_length=8, choices=MESSAGE_STATUSES)
    status_message = models.CharField(max_length=200)
    time_taken_ms = models.PositiveIntegerField(null=True)

    def __str__(self):
        return u'[{}] Job {}, {}'.format(self.status.upper(), self.job.id, self.recipient)

    def send(self):
        start = datetime.now()
        if self.status != 'new':
            raise AttributeError('Message {} has already been run'.format(self.id))
        self.status = 'running'
        self.save()

        if self.recipient.email and '@' in self.recipient.email:
            try:
                send_mail(
                    subject=self.subject,
                    message=self.content_plain,
                    from_email='info@courchevel-1650.com',
                    recipient_list=[self.recipient.email, ],
                    fail_silently=False,
                    html_message=self.content_html
                )
                self.status = 'complete'
            except SMTPException as e:
                self.status = 'failed'
                self.status_message = str(e)
        else:
            self.status = 'failed'
            self.status_message = 'Invalid email address \'{}\''.format(self.recipient.email)

        self.time_taken_ms = int((datetime.now() - start).total_seconds() * 1000)
        self.save()
        return True

    def content_html_safe(self):
        # return SafeString(self.content_html)
        return self.content_html
    content_html_safe.short_description = 'Content HTML'


TRACKER_TYPES = (
    ('link', 'Link'),
    ('image', 'Image'),
    ('pixel', 'Pixel'),
)
TRACKER_SIGNATURE_SECRET = 'dKT4n415M7POZFrW7dUb1jJDmcqVFtJId3HcmPHNVIjjBzNtZSlcz5MICe'


class TrackerManager(models.Manager):
    def add_tracker(self, job_id, type, recipient_id, url=''):
        tracker, _ = Tracker.objects.get_or_create(type=type, job_id=job_id, url=url)
        salt = crypto.get_random_string(6)
        hmac = crypto.salted_hmac(salt, '{}/{}'.format(tracker.id, recipient_id), secret=TRACKER_SIGNATURE_SECRET)
        signature = base64.urlsafe_b64encode(hmac.digest())[:6]
        return 'https://courchevel-1650.com/mailer/r/{}/{}/{}/{}/'.format(
            tracker.id,
            recipient_id,
            salt,
            signature
        )


class Tracker(VersionedModel):
    '''
    Can either be a HREF link that is being redirected, an embedded image that
    is being redirected, or an automatically added 1x1 px tracking pixel image.
    '''
    type = models.CharField(max_length=5, choices=TRACKER_TYPES)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

    objects = TrackerManager()

    def __str__(self):
        return u'{}, {}, {}'.format(self.job, self.type, self.url)

    def track_event(self, recipient_id, salt, signature):
        hmac = crypto.salted_hmac(salt, '{}/{}'.format(self.id, recipient_id), secret=TRACKER_SIGNATURE_SECRET)
        test_signature = base64.urlsafe_b64encode(hmac.digest())[:6]

        if test_signature == signature:
            TrackerEvent(tracker_id=int(self.id), recipient_id=int(recipient_id)).save()
            return True
        return False


class TrackerEvent(models.Model):
    '''
    Registers when a user views a tracked image in their client or clicks a
    tracked link included in the email.
    '''
    created_at = models.DateTimeField(blank=True)
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created:
            self.created = now
        super(TrackerEvent, self).save()
