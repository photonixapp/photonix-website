from django.contrib import admin


class VersionedAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Created/Updated', {
            'classes': ('collapse',),
            'fields': ('created', 'updated')
        }),
    )
    # readonly_fields = ['created', 'updated']
