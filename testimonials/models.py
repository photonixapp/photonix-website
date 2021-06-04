from django.db import models
from utils.models import UUIDModel, VersionedModel


class Testimonial(UUIDModel, VersionedModel):
    """Testimonial model to store comments/reviews that users have made about Photonix."""

    profile_name = models.CharField(max_length=50, verbose_name="Profile Name", help_text='required 50 characters or fewer.')
    profile_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="Profile URL")
    avatar_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="Avatar URL")
    comment = models.TextField(verbose_name="Comment")
    comment_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="Comment URL")

    def __str__(self):
        """To show object."""
        return self.profile_name