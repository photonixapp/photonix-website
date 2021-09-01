import os
from pathlib import Path

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
import maxminddb

from utils.models import UUIDModel


class List(UUIDModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['name']


def generate_token():
    return get_random_string(64)


class Subscription(UUIDModel):
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(blank=True, db_index=True)
    ip = models.CharField(blank=True, max_length=15)
    language = models.CharField(blank=True, max_length=5)
    country = models.CharField(blank=True, max_length=50)
    region = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    landing_page = models.CharField(blank=True, max_length=50)
    source = models.CharField(blank=True, max_length=50)
    medium = models.CharField(blank=True, max_length=50)
    campaign = models.CharField(blank=True, max_length=50)
    unsubscribes = models.ManyToManyField(List, help_text='Which lists the user has unsubscribed from', through='ListUnsubscribes')
    unsubscribed_from_all_lists = models.BooleanField(default=False, help_text='If the user has chosen to unsubscribe from all lists')
    token = models.CharField(max_length=64, default=generate_token, help_text='Lets user update their preferences if they have this token. Prevents mallicious attempts at changing users preferences.')

    def __str__(self):
        return '{}'.format(self.email)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created_at:
            self.created_at = now

        if self.ip and not self.country:
            try:
                geoipreader = maxminddb.open_database(Path(os.path.dirname(__file__)) / '..' / 'geoipdb.mmdb')
                record = geoipreader.get(self.ip)
                if record:
                    self.country = record.get('country', {}).get('names', {}).get('en', None)
                    self.region = record.get('subdivisions', [{}])[0].get('names', {}).get('en', None)
                    self.city = record.get('city', {}).get('names', {}).get('en', None)
            except FileNotFoundError:
                pass

        self.updated_at = now
        super(Subscription, self).save()


class ListUnsubscribes(UUIDModel):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created_at:
            self.created_at = now
