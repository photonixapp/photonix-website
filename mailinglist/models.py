import os
from pathlib import Path

from django.db import models
from django.utils import timezone
import maxminddb

from utils.models import UUIDModel


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
