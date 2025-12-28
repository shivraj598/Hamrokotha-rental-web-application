"""
Custom User model for HamroKotha platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.core.choices import UserType, District


class User(AbstractUser):
    """
    Custom User model with additional fields for rental platform.
    """
    
    # Phone number validator for Nepal
    phone_regex = RegexValidator(
        regex=r'^(\+977)?[0-9]{10}$',
        message="Phone number must be in format: '+977XXXXXXXXXX' or '9XXXXXXXXX'"
    )
    
    # User type
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.TENANT,
        help_text="Select whether you are a landlord or tenant"
    )
    
    # Contact information
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_regex],
        blank=True,
        help_text="Nepal phone number"
    )
    
    # Profile
    profile_picture = models.ImageField(
        upload_to='profiles/%Y/%m/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    
    # Address
    district = models.CharField(
        max_length=20,
        choices=District.choices,
        blank=True,
        help_text="District in Kathmandu Valley"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Full address"
    )
    
    # Verification status
    is_verified = models.BooleanField(
        default=False,
        help_text="Has the user been verified?"
    )
    is_banned = models.BooleanField(
        default=False,
        help_text="Is the user banned?"
    )
    ban_reason = models.TextField(
        blank=True,
        help_text="Reason for ban"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"
    
    def get_full_name(self):
        """Return the user's full name."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username
    
    @property
    def is_landlord(self):
        """Check if user is a landlord."""
        return self.user_type == UserType.LANDLORD
    
    @property
    def is_tenant(self):
        """Check if user is a tenant."""
        return self.user_type == UserType.TENANT
    
    @property
    def is_admin_user(self):
        """Check if user is an admin."""
        return self.user_type == UserType.ADMIN or self.is_staff
    
    @property
    def properties_count(self):
        """Get count of user's properties (for landlords)."""
        if self.is_landlord:
            return self.properties.count()
        return 0
    
    @property
    def active_properties_count(self):
        """Get count of approved properties."""
        if self.is_landlord:
            from apps.core.choices import PropertyStatus
            return self.properties.filter(status=PropertyStatus.APPROVED).count()
        return 0
    
    @property
    def inquiries_count(self):
        """Get count of inquiries made or received."""
        if self.is_tenant:
            return self.inquiries_sent.count()
        elif self.is_landlord:
            from apps.inquiries.models import Inquiry
            return Inquiry.objects.filter(rental_property__owner=self).count()
        return 0
