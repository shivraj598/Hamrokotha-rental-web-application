"""
Core app admin configuration.
"""

from django.contrib import admin
from .models import Report, SiteConfiguration


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'reason', 'status', 'reported_by', 'created_at']
    list_filter = ['content_type', 'reason', 'status', 'created_at']
    search_fields = ['description', 'reported_by__email']
    readonly_fields = ['created_at', 'resolved_at']
    raw_id_fields = ['reported_by', 'reviewed_by']
    
    fieldsets = (
        ('Report Details', {
            'fields': ('content_type', 'object_id', 'reason', 'description')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes', 'reviewed_by')
        }),
        ('Reporter', {
            'fields': ('reported_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'registration_open']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
