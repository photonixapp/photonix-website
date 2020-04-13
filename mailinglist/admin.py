from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'country')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


admin.site.register(Subscription, SubscriptionAdmin)
