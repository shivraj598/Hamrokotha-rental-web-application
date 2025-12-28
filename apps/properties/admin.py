"""
Admin configuration for Property models.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Property, PropertyImage, Favorite, PropertyView


class PropertyImageInline(admin.TabularInline):
    """Inline admin for property images."""
    model = PropertyImage
    extra = 1
    fields = ['image', 'caption', 'is_primary', 'order']
    readonly_fields = ['uploaded_at']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """Admin for Property model."""
    
    list_display = [
        'title', 'owner_name', 'district', 'area', 
        'property_type', 'price_display', 'status_badge', 
        'views_count', 'created_at'
    ]
    list_filter = ['status', 'district', 'property_type', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'area', 'address', 'owner__username', 'owner__email']
    readonly_fields = ['id', 'slug', 'views_count', 'inquiries_count', 'created_at', 'updated_at', 'approved_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'owner', 'title', 'slug', 'description', 'property_type')
        }),
        ('Location', {
            'fields': ('district', 'area', 'address', 'google_maps_link')
        }),
        ('Pricing', {
            'fields': ('price_per_month', 'negotiable', 'security_deposit')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'floor_number', 'total_floors', 'area_sq_ft')
        }),
        ('Amenities & Preferences', {
            'fields': ('amenities', 'parking_available', 'pets_allowed', 'preferred_tenant', 'available_from', 'minimum_stay_months')
        }),
        ('Status & Moderation', {
            'fields': ('status', 'rejection_reason', 'is_featured', 'approved_at')
        }),
        ('Statistics', {
            'fields': ('views_count', 'inquiries_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_properties', 'reject_properties', 'feature_properties', 'unfeature_properties']
    
    def owner_name(self, obj):
        return obj.owner.get_full_name() or obj.owner.username
    owner_name.short_description = 'Owner'
    owner_name.admin_order_field = 'owner__username'
    
    def price_display(self, obj):
        return f"Rs. {obj.price_per_month:,.0f}"
    price_display.short_description = 'Rent/Month'
    price_display.admin_order_field = 'price_per_month'
    
    def status_badge(self, obj):
        colors = {
            'PENDING': '#f59e0b',
            'APPROVED': '#10b981',
            'REJECTED': '#ef4444',
            'RENTED': '#3b82f6',
            'EXPIRED': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def approve_properties(self, request, queryset):
        count = queryset.update(status='APPROVED', approved_at=timezone.now())
        self.message_user(request, f'{count} properties approved.')
    approve_properties.short_description = 'Approve selected properties'
    
    def reject_properties(self, request, queryset):
        count = queryset.update(status='REJECTED')
        self.message_user(request, f'{count} properties rejected.')
    reject_properties.short_description = 'Reject selected properties'
    
    def feature_properties(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, 'Selected properties are now featured.')
    feature_properties.short_description = 'Mark as featured'
    
    def unfeature_properties(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, 'Selected properties are no longer featured.')
    unfeature_properties.short_description = 'Remove from featured'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    """Admin for PropertyImage model."""
    
    list_display = ['property', 'caption', 'is_primary', 'order', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['property__title', 'caption']
    ordering = ['property', 'order']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin for Favorite model."""
    
    list_display = ['user', 'property', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'property__title']
    ordering = ['-created_at']


@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    """Admin for PropertyView model."""
    
    list_display = ['property', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['property__title', 'user__username', 'ip_address']
    ordering = ['-viewed_at']
    readonly_fields = ['property', 'user', 'ip_address', 'user_agent', 'viewed_at']
