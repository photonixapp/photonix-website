
from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Testimonial
from utils.admin import VersionedAdmin


class TestimonialAdmin(VersionedAdmin):
    list_display = ('profile_name', 'comment', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('profile_name', 'comment')
    ordering = ('-created_at',)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    fieldsets = (
        (None, {
            'fields': ('profile_name', 'profile_url', 'avatar_url', 'comment', 'comment_url',),
        }),
    ) + VersionedAdmin.fieldsets


admin.site.register(Testimonial, TestimonialAdmin)