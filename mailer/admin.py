from django.contrib import admin

from utils.admin import VersionedAdmin
from .models import Template, Job, Message, Tracker, TrackerEvent


class TemplateAdmin(VersionedAdmin):
    list_display = ('subject', 'type', 'created_at', 'content_summary')
    list_filter = ('type', 'created_at')
    search_fields = ('subject', 'content_plain', 'content_html')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('type', 'subject',),
        }),
        (None, {
            'fields': ('content_plain', 'content_html',),
        }),
    ) + VersionedAdmin.fieldsets

    def content_summary(self, obj):
        if len(obj.content_plain) <= 100:
            return obj.content_plain
        summary = obj.content_plain[:101].rsplit(' ', 1)[0] + '...'
        return summary


class JobAdmin(VersionedAdmin):
    list_display = ('template', 'status', 'num_recipients', 'num_messages_sent', 'num_recipients_read', 'percent_complete', 'created_at', 'time_taken_ms')
    list_filter = ('status', 'created_at')
    search_fields = ('template__subject',)
    ordering = ('-created_at',)
    readonly_fields = ('template', 'status', 'recipients', 'recipients_read', 'time_taken_ms', 'created_at', 'updated_at')

    fieldsets = []


class MessageAdmin(VersionedAdmin):
    list_display = ('recipient', 'job', 'status', 'created_at', 'time_taken_ms')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('recipient', 'job', 'subject', 'content_plain', 'content_html_safe', 'status', 'status_message', 'time_taken_ms', 'created_at', 'updated_at')
    exclude = ('content_html',)

    fieldsets = []


class TrackerAdmin(VersionedAdmin):
    list_display = ('type', 'job', 'url', 'created_at')
    list_filter = ('type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('type', 'job', 'url', 'created_at', 'updated_at')

    fieldsets = []


class TrackerEventAdmin(admin.ModelAdmin):
    list_display = ('tracker', 'recipient', 'created_at')
    list_filter = ('tracker__type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('tracker', 'recipient', 'created_at')


admin.site.register(Template, TemplateAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(TrackerEvent, TrackerEventAdmin)
