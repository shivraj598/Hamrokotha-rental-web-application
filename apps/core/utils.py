"""
Utility functions for HamroKotha platform.
"""

import re
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def format_npr(amount):
    """
    Format amount in Nepali Rupees.
    Example: 25000 -> 'NPR 25,000'
    """
    if amount is None:
        return 'NPR 0'
    
    # Format with commas (Indian/Nepali style)
    amount_str = str(int(amount))
    if len(amount_str) <= 3:
        return f'NPR {amount_str}'
    
    # Last 3 digits
    result = amount_str[-3:]
    amount_str = amount_str[:-3]
    
    # Add commas every 2 digits for remaining
    while amount_str:
        result = amount_str[-2:] + ',' + result
        amount_str = amount_str[:-2]
    
    return f'NPR {result}'


def validate_nepal_phone(phone):
    """
    Validate Nepal phone number format.
    Accepts: +977-XXXXXXXXXX, 977XXXXXXXXXX, 9XXXXXXXXX, 01-XXXXXXX
    """
    # Remove spaces and dashes
    phone = re.sub(r'[\s\-]', '', phone)
    
    # Mobile number patterns
    mobile_pattern = r'^(\+?977)?9[78]\d{8}$'
    # Landline pattern
    landline_pattern = r'^(\+?977)?0?1\d{7}$'
    
    if re.match(mobile_pattern, phone) or re.match(landline_pattern, phone):
        return True
    return False


def format_nepal_phone(phone):
    """
    Format phone number to standard Nepal format.
    Returns: +977-98XXXXXXXX or +977-1-XXXXXXX
    """
    # Remove all non-digits except +
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Remove leading + if present
    if phone.startswith('+'):
        phone = phone[1:]
    
    # Remove 977 prefix if present
    if phone.startswith('977'):
        phone = phone[3:]
    
    # Mobile number
    if phone.startswith('9') and len(phone) == 10:
        return f'+977-{phone}'
    
    # Landline
    if phone.startswith('01') or phone.startswith('1'):
        if phone.startswith('0'):
            phone = phone[1:]
        return f'+977-1-{phone[1:]}'
    
    return phone


def send_email_notification(subject, template_name, context, recipient_list):
    """
    Send email notification using template.
    """
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def truncate_text(text, max_length=100):
    """
    Truncate text to specified length with ellipsis.
    """
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'


def generate_property_slug(title, property_id):
    """
    Generate URL-friendly slug for property.
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    return f"{slug}-{property_id}"
