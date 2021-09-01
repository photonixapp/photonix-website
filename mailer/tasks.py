from __future__ import absolute_import

from celery import shared_task


@shared_task
def start_job(job_id):
    from mailer.models import Job
    job = Job.objects.get(id=job_id)
    job.start()


@shared_task
def send_message(message_id):
    from mailer.models import Message
    message = Message.objects.get(id=message_id)
    message.send()
