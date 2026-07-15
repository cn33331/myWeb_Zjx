from django.contrib import admin
from .models import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'upload_date', 'downloads')
    list_filter = ('upload_date',)
    search_fields = ('name', 'description')
    readonly_fields = ('downloads',)
