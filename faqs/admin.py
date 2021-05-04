
from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from faqs.models import Question
from utils.admin import VersionedAdmin


class QuestionAdmin(VersionedAdmin):
    """To show question model in django-admin."""

    list_display = ('question', 'answer', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('question', 'slug')
    ordering = ('-created_at',)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'slug'),
        }),
    ) + VersionedAdmin.fieldsets
    
    readonly_fields = ['slug']


admin.site.register(Question, QuestionAdmin)
