from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Post
from utils.admin import VersionedAdmin


class PostAdmin(VersionedAdmin):
    list_display = ('title', 'slug', 'status', 'created', 'updated')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('title', 'slug', 'status')
    ordering = ('-created',)
    prepopulated_fields = {"slug": ("title",)}

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'content', 'photo',),
        }),
    ) + VersionedAdmin.fieldsets


admin.site.register(Post, PostAdmin)
