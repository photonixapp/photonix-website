from mock import patch
import re

from django.test import TestCase

from mailer.models import Customer, Template, Job, Message


class ContentTestCase(TestCase):

    def setUp(self):
        self.customer1, _ = Customer.objects.get_or_create(firstname='Bob', surname='Smith')
        self.customer2, _ = Customer.objects.get_or_create(firstname='James', surname='Balls')
        content_plain = 'Hello {{ customer.firstname }}'
        content_html = '<p>Hello {{ customer.firstname }}</p>'
        self.template, _ = Template.objects.get_or_create(type='mass_email', subject='Template 1', content_plain=content_plain, content_html=content_html)
        self.job, _ = Job.objects.get_or_create(template=self.template, status='new')
        self.job.recipients.add(self.customer1)
        self.job.recipients.add(self.customer2)

    def test_templating(self):
        with patch('mailer.models.Job.tasks_are_completed') as tasks_are_completed:
            tasks_are_completed.return_value = True
            self.job.start()
        self.assertEqual(Message.objects.filter(job=self.job.id).count(), 2)

        content_html = Message.objects.get(job=self.job.id, recipient=self.customer1).content_html
        content_plain = Message.objects.get(job=self.job.id, recipient=self.customer1).content_plain

        self.assertIn('Hello Bob', content_plain)
        self.assertIn('John and Julie Moore', content_plain)  # Plain Footer
        self.assertIn('<p>Hello Bob</p>', content_html)
        self.assertIn('John and Julie Moore', content_html)  # HTML Footer
        self.assertIn('src="data:image/png;base64,iVBORw0KG', content_html)  # HTML Footer

    def test_url_redirects(self):
        content_plain = 'Hello {{ customer.firstname }}, Look at http://example.com/'
        content_html = '<p>Hello {{ customer.firstname }},</p><p>Look at <a href="http://example.com/">http://example.com/</a></p>'
        template, _ = Template.objects.get_or_create(type='mass_email', subject='Template 1', content_plain=content_plain, content_html=content_html)
        job, _ = Job.objects.get_or_create(template=template, status='new')
        job.recipients.add(self.customer1)

        with patch('mailer.models.Job.tasks_are_completed') as tasks_are_completed:
            tasks_are_completed.return_value = True
            job.start()

        content_html = Message.objects.get(job=job.id, recipient=self.customer1).content_html
        content_plain = Message.objects.get(job=job.id, recipient=self.customer1).content_plain

        # Test tracking pixel got added to HTML version
        self.assertIn('<img src="https://courchevel-1650.com/mailer/r/', content_html)

        # URLs getting replaces in plain email
        self.assertNotIn('example.com', content_plain)
        self.assertIn('https://courchevel-1650.com/mailer/r/', content_plain)

        # Link HREFs being replaced whilst keeping the link text the same
        self.assertTrue(re.search(r'<a href\="https:\/\/courchevel-1650\.com\/mailer\/r\/' + str(job.id) + r'\/' + str(self.customer1.id) + r'\/\S{6}\/\S{6}\/">http:\/\/example\.com\/<\/a>', content_html) is not None)
