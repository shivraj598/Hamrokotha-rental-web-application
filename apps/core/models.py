"""
Core models - Report model for fraud detection.
"""

from django.db import models
from django.conf import settings
from apps.core.choices import ReportReason, ReportStatus


class Report(models.Model):
    """
    Report model for flagging suspicious content.
    Can be used to report properties, users, or inquiries.
    """
    CONTENT_TYPE_CHOICES = [
        ('property', 'Property'),
        ('user', 'User'),
        ('inquiry', 'Inquiry'),
    ]
    
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    object_id = models.PositiveIntegerField()
    reason = models.CharField(max_length=20, choices=ReportReason.choices)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
    
    def __str__(self):
        return f"Report #{self.id} - {self.content_type} ({self.status})"


class SiteConfiguration(models.Model):
    """
    Singleton model for site-wide configuration.
    """
    site_name = models.CharField(max_length=100, default='HamroKotha')
    site_description = models.TextField(
        default='Find your perfect rental property in Kathmandu Valley'
    )
    contact_email = models.EmailField(default='contact@hamrokotha.com')
    contact_phone = models.CharField(max_length=20, default='+977-1-XXXXXXX')
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Feature toggles
    registration_open = models.BooleanField(default=True)
    property_approval_required = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'
    
    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Get or create the configuration instance."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
    
    def __str__(self):
        return self.site_name
