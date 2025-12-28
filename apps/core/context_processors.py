"""
Context processors for global template variables.
"""

from django.conf import settings


def site_settings(request):
    """
    Add site-wide settings to template context.
    """
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'HamroKotha'),
        'SITE_URL': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        'DEBUG': settings.DEBUG,
    }
