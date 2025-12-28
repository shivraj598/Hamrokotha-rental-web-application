"""
Accounts app admin configuration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin configuration."""
    
    list_display = [
        'username', 'email', 'get_full_name', 'user_type', 
        'phone_number', 'district', 'is_verified', 'is_banned', 
        'is_active', 'date_joined'
    ]
    list_filter = ['user_type', 'is_verified', 'is_banned', 'is_active', 'district', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')
        }),
        ('User Type & Address', {
            'fields': ('user_type', 'district', 'address')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_banned', 'ban_reason')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 
                'user_type', 'phone_number', 'password1', 'password2'
            ),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    actions = ['verify_users', 'ban_users', 'unban_users']
    
    @admin.action(description='Verify selected users')
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} users verified successfully.")
    
    @admin.action(description='Ban selected users')
    def ban_users(self, request, queryset):
        queryset.update(is_banned=True, is_active=False)
        self.message_user(request, f"{queryset.count()} users banned.")
    
    @admin.action(description='Unban selected users')
    def unban_users(self, request, queryset):
        queryset.update(is_banned=False, is_active=True, ban_reason='')
        self.message_user(request, f"{queryset.count()} users unbanned.")
