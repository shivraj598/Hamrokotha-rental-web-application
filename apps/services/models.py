import uuid
from django.db import models
from django.conf import settings


class FindRoomRequest(models.Model):
    """Request from a tenant looking for a room/property."""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWING', 'Under Review'),
        ('MATCHED', 'Matched'),
        ('CLOSED', 'Closed'),
    ]
    
    BUDGET_CHOICES = [
        ('5000-10000', 'Rs. 5,000 - 10,000'),
        ('10000-15000', 'Rs. 10,000 - 15,000'),
        ('15000-20000', 'Rs. 15,000 - 20,000'),
        ('20000-30000', 'Rs. 20,000 - 30,000'),
        ('30000-50000', 'Rs. 30,000 - 50,000'),
        ('50000+', 'Rs. 50,000+'),
    ]
    
    PROPERTY_TYPES = [
        ('ROOM', 'Single Room'),
        ('FLAT', 'Flat/Apartment'),
        ('HOUSE', 'Full House'),
        ('ANY', 'Any Type'),
    ]
    
    DISTRICT_CHOICES = [
        ('KATHMANDU', 'Kathmandu'),
        ('BHAKTAPUR', 'Bhaktapur'),
        ('LALITPUR', 'Lalitpur'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='find_room_requests'
    )
    
    # Contact
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Requirements
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES)
    preferred_areas = models.TextField(help_text="Comma-separated list of preferred areas")
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    bedrooms = models.PositiveIntegerField(default=1)
    
    # Preferences
    move_in_date = models.DateField()
    duration_months = models.PositiveIntegerField(default=12, help_text="Expected stay duration in months")
    additional_requirements = models.TextField(blank=True, help_text="Any specific requirements")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Find Room Request'
        verbose_name_plural = 'Find Room Requests'
    
    def __str__(self):
        return f"Room Request by {self.name} in {self.get_district_display()}"


class ShiftHomeRequest(models.Model):
    """Request for home shifting/moving services."""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('QUOTED', 'Quote Sent'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    SHIFT_TYPE_CHOICES = [
        ('LOCAL', 'Within Same District'),
        ('INTER_DISTRICT', 'Between Districts'),
        ('OUTSIDE_VALLEY', 'Outside Kathmandu Valley'),
    ]
    
    PROPERTY_SIZE_CHOICES = [
        ('ROOM', 'Single Room'),
        ('1BHK', '1 BHK'),
        ('2BHK', '2 BHK'),
        ('3BHK', '3 BHK'),
        ('HOUSE', 'Full House'),
    ]
    
    DISTRICT_CHOICES = [
        ('KATHMANDU', 'Kathmandu'),
        ('BHAKTAPUR', 'Bhaktapur'),
        ('LALITPUR', 'Lalitpur'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shift_home_requests'
    )
    
    # Contact
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Shift Details
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES)
    property_size = models.CharField(max_length=20, choices=PROPERTY_SIZE_CHOICES)
    
    # From Location
    from_district = models.CharField(max_length=20, choices=DISTRICT_CHOICES)
    from_area = models.CharField(max_length=100)
    from_address = models.TextField()
    
    # To Location
    to_district = models.CharField(max_length=20, choices=DISTRICT_CHOICES)
    to_area = models.CharField(max_length=100)
    to_address = models.TextField()
    
    # Schedule
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, blank=True)
    flexible_date = models.BooleanField(default=False)
    
    # Additional
    has_heavy_items = models.BooleanField(default=False, help_text="Refrigerator, washing machine, etc.")
    needs_packing = models.BooleanField(default=False, help_text="Need packing service?")
    special_items = models.TextField(blank=True, help_text="Any special items that need careful handling")
    additional_notes = models.TextField(blank=True)
    
    # Pricing
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shift Home Request'
        verbose_name_plural = 'Shift Home Requests'
    
    def __str__(self):
        return f"Shift from {self.from_area} to {self.to_area} by {self.name}"
