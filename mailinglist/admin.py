from django.contrib import admin

from .models import List, Subscription, ListUnsubscribes
from .models import Subscription


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class ListUnsubscribesInline(admin.TabularInline):
    model = ListUnsubscribes
    extra = 2


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'country', 'num_unsubscribes', 'unsubscribed_from_all_lists', 'landing_page')
    list_filter = ('created_at', 'unsubscribed_from_all_lists', 'landing_page')
    ordering = ('-created_at',)
    filter_horizontal = ('unsubscribes',)
    inlines = (ListUnsubscribesInline,)

    def num_unsubscribes(self, obj):
        return obj.unsubscribes.count()
