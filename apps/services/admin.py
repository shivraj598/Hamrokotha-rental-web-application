from django.contrib import admin
from django.utils.html import format_html
from .models import FindRoomRequest, ShiftHomeRequest


@admin.register(FindRoomRequest)
class FindRoomRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'phone', 'district', 'property_type',
        'budget_range', 'status_badge', 'move_in_date', 'created_at'
    ]
    list_filter = ['status', 'district', 'property_type', 'budget_range', 'created_at']
    search_fields = ['name', 'email', 'phone', 'preferred_areas']
    readonly_fields = [
        'id', 'user', 'name', 'email', 'phone',
        'property_type', 'district', 'preferred_areas',
        'budget_range', 'bedrooms', 'move_in_date',
        'duration_months', 'additional_requirements',
        'created_at', 'updated_at'
    ]
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('id', 'user', 'status')
        }),
        ('Contact Details', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Requirements', {
            'fields': ('property_type', 'district', 'preferred_areas', 'budget_range', 'bedrooms')
        }),
        ('Schedule', {
            'fields': ('move_in_date', 'duration_months')
        }),
        ('Additional Information', {
            'fields': ('additional_requirements', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'PENDING': '#f59e0b',
            'REVIEWING': '#3b82f6',
            'MATCHED': '#10b981',
            'CLOSED': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_reviewing', 'mark_matched', 'mark_closed']
    
    @admin.action(description='Mark selected as Under Review')
    def mark_reviewing(self, request, queryset):
        updated = queryset.update(status='REVIEWING')
        self.message_user(request, f'{updated} requests marked as under review.')
    
    @admin.action(description='Mark selected as Matched')
    def mark_matched(self, request, queryset):
        updated = queryset.update(status='MATCHED')
        self.message_user(request, f'{updated} requests marked as matched.')
    
    @admin.action(description='Mark selected as Closed')
    def mark_closed(self, request, queryset):
        updated = queryset.update(status='CLOSED')
        self.message_user(request, f'{updated} requests marked as closed.')


@admin.register(ShiftHomeRequest)
class ShiftHomeRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'phone', 'shift_type', 'property_size',
        'route_display', 'preferred_date', 'status_badge', 'estimated_cost', 'created_at'
    ]
    list_filter = ['status', 'shift_type', 'property_size', 'from_district', 'to_district', 'created_at']
    search_fields = ['name', 'email', 'phone', 'from_area', 'to_area']
    readonly_fields = [
        'id', 'user', 'name', 'email', 'phone',
        'shift_type', 'property_size',
        'from_district', 'from_area', 'from_address',
        'to_district', 'to_area', 'to_address',
        'preferred_date', 'preferred_time', 'flexible_date',
        'has_heavy_items', 'needs_packing', 'special_items',
        'additional_notes', 'created_at', 'updated_at'
    ]
    list_per_page = 25
    date_hierarchy = 'preferred_date'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('id', 'user', 'status')
        }),
        ('Contact Details', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Shift Details', {
            'fields': ('shift_type', 'property_size')
        }),
        ('From Location', {
            'fields': ('from_district', 'from_area', 'from_address')
        }),
        ('To Location', {
            'fields': ('to_district', 'to_area', 'to_address')
        }),
        ('Schedule', {
            'fields': ('preferred_date', 'preferred_time', 'flexible_date')
        }),
        ('Additional Services', {
            'fields': ('has_heavy_items', 'needs_packing', 'special_items', 'additional_notes')
        }),
        ('Pricing', {
            'fields': ('estimated_cost', 'final_cost', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def route_display(self, obj):
        return f"{obj.from_area} → {obj.to_area}"
    route_display.short_description = 'Route'
    
    def status_badge(self, obj):
        colors = {
            'PENDING': '#f59e0b',
            'QUOTED': '#3b82f6',
            'CONFIRMED': '#8b5cf6',
            'COMPLETED': '#10b981',
            'CANCELLED': '#ef4444',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_quoted', 'mark_confirmed', 'mark_completed', 'mark_cancelled']
    
    @admin.action(description='Mark selected as Quote Sent')
    def mark_quoted(self, request, queryset):
        updated = queryset.update(status='QUOTED')
        self.message_user(request, f'{updated} requests marked as quoted.')
    
    @admin.action(description='Mark selected as Confirmed')
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='CONFIRMED')
        self.message_user(request, f'{updated} requests marked as confirmed.')
    
    @admin.action(description='Mark selected as Completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f'{updated} requests marked as completed.')
    
    @admin.action(description='Mark selected as Cancelled')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f'{updated} requests marked as cancelled.')
