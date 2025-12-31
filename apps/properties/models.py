"""
Property models for the rental platform.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from apps.core.choices import District, PropertyType, PropertyStatus, AMENITIES
import uuid
import hashlib


class Property(models.Model):
    """Main property model for rental listings."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(help_text="Detailed description of the property")
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.ROOM
    )
    
    # Location
    district = models.CharField(
        max_length=20,
        choices=District.choices,
        default=District.KATHMANDU
    )
    area = models.CharField(max_length=100, help_text="e.g., Thamel, Basundhara, Jhamsikhel")
    address = models.CharField(max_length=255, help_text="Full address/landmark")
    google_maps_link = models.URLField(blank=True, null=True)
    
    # Pricing
    price_per_month = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Monthly rent in Nepali Rupees"
    )
    negotiable = models.BooleanField(default=False)
    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Security deposit amount (optional)"
    )
    
    # Property Details
    bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    floor_number = models.CharField(max_length=20, blank=True, help_text="e.g., Ground, 1st, 2nd")
    total_floors = models.PositiveSmallIntegerField(default=1)
    area_sq_ft = models.PositiveIntegerField(blank=True, null=True, help_text="Area in square feet")
    
    # Amenities (stored as JSON list)
    amenities = models.JSONField(
        default=list,
        blank=True,
        help_text="List of amenity codes"
    )
    
    # Rules and Preferences
    parking_available = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    preferred_tenant = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., Family, Bachelor, Student, Any"
    )
    available_from = models.DateField(blank=True, null=True)
    minimum_stay_months = models.PositiveSmallIntegerField(default=6)
    
    # Status and Moderation
    status = models.CharField(
        max_length=20,
        choices=PropertyStatus.choices,
        default=PropertyStatus.PENDING
    )
    rejection_reason = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    # Fraud / Moderation flags
    is_flagged = models.BooleanField(default=False)
    fraud_reason = models.TextField(blank=True, null=True)
    flag_count = models.PositiveIntegerField(default=0)
    flagged_at = models.DateTimeField(blank=True, null=True)
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0)
    inquiries_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['district', 'status']),
            models.Index(fields=['property_type', 'status']),
            models.Index(fields=['price_per_month']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.area}, {self.get_district_display()}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.area}")
            unique_slug = base_slug
            counter = 1
            while Property.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'pk': self.pk})
    
    @property
    def primary_image(self):
        """Get the primary image or first image."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()
    
    @property
    def amenities_display(self):
        """Get human-readable list of amenities."""
        amenity_dict = dict(AMENITIES)
        return [amenity_dict.get(code, code) for code in self.amenities if code in amenity_dict]
    
    @property
    def is_available(self):
        """Check if property is available for rent."""
        return self.status == PropertyStatus.APPROVED
    
    def increment_views(self):
        """Increment view count."""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class PropertyImage(models.Model):
    """Images for property listings."""
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='properties/%Y/%m/')
    image_hash = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-is_primary', '-uploaded_at']
    
    def __str__(self):
        return f"Image for {self.property.title}"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset others
        if self.is_primary:
            PropertyImage.objects.filter(
                property=self.property, 
                is_primary=True
            ).update(is_primary=False)

        # Compute SHA256 hash of the image file if present
        try:
            if self.image and (not self.image_hash or hasattr(self.image.file, 'read')):
                self.image.file.seek(0)
                data = self.image.file.read()
                sha = hashlib.sha256(data).hexdigest()
                self.image_hash = sha
        except Exception:
            # If hashing fails, silently continue (don't block saves)
            pass

        super().save(*args, **kwargs)

        # Detection: find duplicate images by exact hash on other properties
        if self.image_hash:
            duplicates = PropertyImage.objects.filter(image_hash=self.image_hash).exclude(pk=self.pk)
            for dup in duplicates.select_related('property__owner'):
                # If duplicate belongs to a different owner, flag both properties
                if dup.property.owner != self.property.owner:
                    now = timezone.now()

                    # Flag this property
                    try:
                        self.property.is_flagged = True
                        self.property.flag_count = (self.property.flag_count or 0) + 1
                        msg = f"Duplicate image detected with property {dup.property.id} (owner: {dup.property.owner.username})"
                        self.property.fraud_reason = (self.property.fraud_reason or '') + '\n' + msg
                        self.property.flagged_at = now
                        self.property.save(update_fields=['is_flagged', 'flag_count', 'fraud_reason', 'flagged_at'])
                    except Exception:
                        pass

                    # Flag the duplicate's property as well
                    try:
                        dup.property.is_flagged = True
                        dup.property.flag_count = (dup.property.flag_count or 0) + 1
                        msg2 = f"Duplicate image detected with property {self.property.id} (owner: {self.property.owner.username})"
                        dup.property.fraud_reason = (dup.property.fraud_reason or '') + '\n' + msg2
                        dup.property.flagged_at = now
                        dup.property.save(update_fields=['is_flagged', 'flag_count', 'fraud_reason', 'flagged_at'])
                    except Exception:
                        pass


class Favorite(models.Model):
    """User's favorite/saved properties."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class PropertyView(models.Model):
    """Track property views for analytics."""
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='view_logs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"View on {self.property.title} at {self.viewed_at}"
