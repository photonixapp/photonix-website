from django.test import TestCase

from mailer.models import Customer, Template, Job, Tracker


class TrackingTestCase(TestCase):

    def setUp(self):
        self.customer1, _ = Customer.objects.get_or_create(firstname='Bob', surname='Smith')
        self.customer2, _ = Customer.objects.get_or_create(firstname='James', surname='Balls')
        self.template, _ = Template.objects.get_or_create(type='mass_email', subject='Template 1', content_plain='Hello')
        self.job, _ = Job.objects.get_or_create(template=self.template, status='complete')
        self.job.recipients.add(self.customer1)
        self.job.recipients.add(self.customer2)

    def test_tracking(self):
        self.assertEqual(self.job.num_recipients_read(), 0)

        customer1_link1 = Tracker.objects.add_tracker(self.job.id, 'link', self.customer1.id, 'http://example.com/').split('/')[5:9]
        # Last 4 components from a URL like this: https://courchevel-1650.com/mailer/r/1/1/nRuO3R/p8OB8U/
        tracker = Tracker.objects.get(id=customer1_link1[0])

        # User tries to manipulate a URL
        tracker.track_event(self.customer1.id, customer1_link1[2], 'XXX')
        self.assertEqual(self.job.num_recipients_read(), 0)

        # Track first recipient clicking a link
        tracker.track_event(self.customer1.id, customer1_link1[2], customer1_link1[3])
        self.assertEqual(self.job.num_recipients_read(), 1)

        # Track first recipient clicking another link from same email
        customer1_link2 = Tracker.objects.add_tracker(self.job.id, 'link', self.customer1.id, 'http://example2.com/').split('/')[5:9]
        tracker = Tracker.objects.get(id=customer1_link2[0])
        tracker.track_event(self.customer1.id, customer1_link2[2], customer1_link2[3])
        self.assertEqual(self.job.num_recipients_read(), 1)

        # Track second recipient clicking a link
        customer2_link1 = Tracker.objects.add_tracker(self.job.id, 'link', self.customer2.id, 'http://example.com/').split('/')[5:9]
        self.assertEqual(customer1_link1[0], customer2_link1[0])  # Tracker should be reused from customer 1 with the same link
        tracker = Tracker.objects.get(id=customer2_link1[0])
        tracker.track_event(self.customer2.id, customer2_link1[2], customer2_link1[3])
        self.assertEqual(self.job.num_recipients_read(), 2)
