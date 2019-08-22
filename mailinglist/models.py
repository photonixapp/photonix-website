from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    email = models.EmailField(db_index=True)
    created_at = models.DateTimeField(blank=True, db_index=True)

    def __str__(self):
        return '{}'.format(self.email)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        super(Subscription, self).save()
