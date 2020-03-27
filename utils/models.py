from django.db import models
from django.utils import timezone


class VersionedModel(models.Model):
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created:
            self.created = now
        self.updated = now
        super(VersionedModel, self).save()
