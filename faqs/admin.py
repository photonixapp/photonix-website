from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from faqs.models import Question
from utils.admin import VersionedAdmin


class QuestionAdmin(VersionedAdmin):
    """To show question model in django-admin."""

    list_display = ('title', 'answer_short', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'answer', 'slug')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    fieldsets = (
        (None, {
            'fields': ('title', 'answer', 'slug'),
        }),
    ) + VersionedAdmin.fieldsets

    def answer_short(self, obj):
        return obj.answer[:100] + '…'


admin.site.register(Question, QuestionAdmin)
