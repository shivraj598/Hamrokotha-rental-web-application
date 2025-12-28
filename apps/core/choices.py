"""
Choices and constants for HamroKotha Rental Platform.
Kathmandu Valley specific data.
"""

from django.db import models


class UserType(models.TextChoices):
    """User type choices."""
    LANDLORD = 'LANDLORD', 'Landlord'
    TENANT = 'TENANT', 'Tenant'
    ADMIN = 'ADMIN', 'Admin'


class District(models.TextChoices):
    """Kathmandu Valley districts."""
    KATHMANDU = 'Kathmandu', 'Kathmandu'
    BHAKTAPUR = 'Bhaktapur', 'Bhaktapur'
    LALITPUR = 'Lalitpur', 'Lalitpur'


class PropertyType(models.TextChoices):
    """Property type choices."""
    ROOM = 'ROOM', 'Room'
    FLAT = 'FLAT', 'Flat'
    APARTMENT = 'APARTMENT', 'Apartment'
    HOUSE = 'HOUSE', 'House'
    COMMERCIAL = 'COMMERCIAL', 'Commercial Space'


class PropertyStatus(models.TextChoices):
    """Property listing status."""
    PENDING = 'PENDING', 'Pending Approval'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    RENTED = 'RENTED', 'Rented Out'


class InquiryStatus(models.TextChoices):
    """Inquiry status choices."""
    PENDING = 'PENDING', 'Pending'
    REPLIED = 'REPLIED', 'Replied'
    CLOSED = 'CLOSED', 'Closed'


class ServiceRequestStatus(models.TextChoices):
    """Service request status."""
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class ReportReason(models.TextChoices):
    """Report reason choices."""
    SPAM = 'SPAM', 'Spam'
    FRAUD = 'FRAUD', 'Fraud'
    INAPPROPRIATE = 'INAPPROPRIATE', 'Inappropriate Content'
    DUPLICATE = 'DUPLICATE', 'Duplicate Listing'
    OTHER = 'OTHER', 'Other'


class ReportStatus(models.TextChoices):
    """Report status choices."""
    PENDING = 'PENDING', 'Pending'
    REVIEWED = 'REVIEWED', 'Reviewed'
    RESOLVED = 'RESOLVED', 'Resolved'
    DISMISSED = 'DISMISSED', 'Dismissed'


class AdminActionType(models.TextChoices):
    """Admin action types for activity logging."""
    USER_CREATED = 'USER_CREATED', 'User Created'
    USER_BANNED = 'USER_BANNED', 'User Banned'
    USER_UNBANNED = 'USER_UNBANNED', 'User Unbanned'
    USER_VERIFIED = 'USER_VERIFIED', 'User Verified'
    PROPERTY_APPROVED = 'PROPERTY_APPROVED', 'Property Approved'
    PROPERTY_REJECTED = 'PROPERTY_REJECTED', 'Property Rejected'
    PROPERTY_DELETED = 'PROPERTY_DELETED', 'Property Deleted'
    INQUIRY_FLAGGED = 'INQUIRY_FLAGGED', 'Inquiry Flagged'
    REPORT_RESOLVED = 'REPORT_RESOLVED', 'Report Resolved'
    SERVICE_COMPLETED = 'SERVICE_COMPLETED', 'Service Request Completed'


# Popular areas by district in Kathmandu Valley
KATHMANDU_AREAS = [
    'Thamel', 'Naxal', 'Baneshwor', 'Koteshwor', 'Chabahil',
    'Balaju', 'Kalimati', 'Putalisadak', 'New Baneshwor', 'Maharajgunj',
    'Budhanilkantha', 'Jorpati', 'Bouddha', 'Swayambhu', 'Kalanki',
    'Kirtipur', 'Gongabu', 'Samakhushi', 'Basundhara', 'Lazimpat',
    'Durbarmarg', 'Jamal', 'Battisputali', 'Gaushala', 'Maitidevi'
]

BHAKTAPUR_AREAS = [
    'Suryabinayak', 'Thimi', 'Changunarayan', 'Sallaghari', 'Duwakot',
    'Lokanthali', 'Katunje', 'Jagati', 'Byasi', 'Sipadol',
    'Tathali', 'Dattatreya', 'Kamalbinayak', 'Nagarkot'
]

LALITPUR_AREAS = [
    'Jhamsikhel', 'Sanepa', 'Jawalakhel', 'Pulchowk', 'Lagankhel',
    'Satdobato', 'Imadol', 'Ekantakuna', 'Kupondole', 'Patan',
    'Mangalbazar', 'Gwarko', 'Tikathali', 'Lubhu', 'Godawari',
    'Balkumari', 'Nakhipot', 'Dhobighat', 'Kupandol'
]

# All areas by district
AREAS_BY_DISTRICT = {
    'Kathmandu': KATHMANDU_AREAS,
    'Bhaktapur': BHAKTAPUR_AREAS,
    'Lalitpur': LALITPUR_AREAS,
}

# Common amenities for properties
AMENITIES = [
    ('wifi', 'WiFi'),
    ('parking', 'Parking'),
    ('water', '24/7 Water'),
    ('electricity', 'Electricity Backup'),
    ('kitchen', 'Kitchen'),
    ('bathroom', 'Attached Bathroom'),
    ('balcony', 'Balcony'),
    ('terrace', 'Terrace'),
    ('garden', 'Garden'),
    ('security', 'Security Guard'),
    ('cctv', 'CCTV'),
    ('elevator', 'Elevator'),
    ('gym', 'Gym'),
    ('laundry', 'Laundry'),
    ('ac', 'Air Conditioning'),
    ('heater', 'Water Heater'),
    ('tv', 'TV/Cable'),
    ('furnished', 'Furnished'),
    ('pet_friendly', 'Pet Friendly'),
    ('family_only', 'Family Only'),
]

# Price ranges in NPR for filtering
PRICE_RANGES = [
    (0, 5000, 'Under NPR 5,000'),
    (5000, 10000, 'NPR 5,000 - 10,000'),
    (10000, 15000, 'NPR 10,000 - 15,000'),
    (15000, 20000, 'NPR 15,000 - 20,000'),
    (20000, 30000, 'NPR 20,000 - 30,000'),
    (30000, 50000, 'NPR 30,000 - 50,000'),
    (50000, 100000, 'NPR 50,000 - 1,00,000'),
    (100000, None, 'Above NPR 1,00,000'),
]

# Bedroom options
BEDROOM_CHOICES = [
    (1, '1 Bedroom'),
    (2, '2 Bedrooms'),
    (3, '3 Bedrooms'),
    (4, '4 Bedrooms'),
    (5, '5+ Bedrooms'),
]

# Bathroom options
BATHROOM_CHOICES = [
    (1, '1 Bathroom'),
    (2, '2 Bathrooms'),
    (3, '3 Bathrooms'),
    (4, '4+ Bathrooms'),
]
