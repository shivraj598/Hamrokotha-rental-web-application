from django.contrib import admin
from .models import Inquiry, InquiryMessage


class InquiryMessageInline(admin.TabularInline):
    model = InquiryMessage
    extra = 0
    readonly_fields = ['sender', 'message', 'is_read', 'created_at']
    can_delete = False


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'property_title', 'sender_name', 'landlord_name', 
        'status_badge', 'is_read', 'created_at'
    ]
    list_filter = ['status', 'is_read', 'created_at', 'property__district']
    search_fields = [
        'property__title', 'sender__email', 'sender__first_name',
        'name', 'email', 'message'
    ]
    readonly_fields = [
        'id', 'property', 'sender', 'name', 'email', 'phone', 
        'message', 'preferred_visit_date', 'preferred_visit_time', 
        'created_at', 'updated_at'
    ]
    list_per_page = 25
    date_hierarchy = 'created_at'
    inlines = [InquiryMessageInline]
    
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('id', 'property', 'sender', 'status', 'is_read')
        }),
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message', 'preferred_visit_date', 'preferred_visit_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def property_title(self, obj):
        return obj.property.title[:30] + '...' if len(obj.property.title) > 30 else obj.property.title
    property_title.short_description = 'Property'
    
    def sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.email
    sender_name.short_description = 'Sender'
    
    def landlord_name(self, obj):
        return obj.property.owner.get_full_name() or obj.property.owner.email
    landlord_name.short_description = 'Landlord'
    
    def status_badge(self, obj):
        colors = {
            'PENDING': 'orange',
            'RESPONDED': 'green',
            'CLOSED': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return f'<span style="background-color: {color}; color: white; padding: 3px 10px; border-radius: 10px;">{obj.get_status_display()}</span>'
    status_badge.short_description = 'Status'
    status_badge.allow_tags = True
    
    actions = ['mark_as_read', 'mark_as_unread', 'close_inquiries']
    
    @admin.action(description='Mark selected inquiries as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} inquiries marked as read.')
    
    @admin.action(description='Mark selected inquiries as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} inquiries marked as unread.')
    
    @admin.action(description='Close selected inquiries')
    def close_inquiries(self, request, queryset):
        updated = queryset.update(status='CLOSED')
        self.message_user(request, f'{updated} inquiries closed.')


@admin.register(InquiryMessage)
class InquiryMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'inquiry_property', 'sender_name', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message', 'sender__email', 'sender__first_name', 'inquiry__property__title']
    readonly_fields = ['id', 'inquiry', 'sender', 'message', 'created_at']
    list_per_page = 25
    
    def inquiry_property(self, obj):
        return obj.inquiry.property.title[:30]
    inquiry_property.short_description = 'Property'
    
    def sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.email
    sender_name.short_description = 'Sender'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
