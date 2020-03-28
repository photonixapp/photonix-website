from django.contrib import admin


class VersionedAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Created/Updated', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
