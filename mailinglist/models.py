import os

from django.db import models
from django.utils import timezone
import requests

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
            api_key = os.environ.get('GEOIP_API_KEY')
            if api_key:
                try:
                    response = requests.get(
                        f'https://geoip.epixstudios.co.uk/{self.ip}',
                        headers={'Authorization': f'Bearer {api_key}'},
                        timeout=5
                    )
                    if response.status_code == 200:
                        data = response.json()
                        self.country = data.get('country')
                        self.region = data.get('subdivision')
                        self.city = data.get('city')
                except requests.RequestException:
                    pass

        self.updated_at = now
        super(Subscription, self).save()
