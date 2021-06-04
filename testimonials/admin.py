
from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Testimonial
from utils.admin import VersionedAdmin


class TestimonialAdmin(VersionedAdmin):
    """To show Testimonial model in django-admin."""
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    fieldsets = (
        (None, {
            'fields': ('profile_name', 'profile_url', 'avatar_url', 'comment', 'comment_url',),
        }),
    ) + VersionedAdmin.fieldsets


admin.site.register(Testimonial, TestimonialAdmin)