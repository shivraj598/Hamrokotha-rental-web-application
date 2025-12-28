"""
Custom template tags for HamroKotha platform.
"""

from django import template
from apps.core.utils import format_npr, truncate_text

register = template.Library()


@register.filter
def npr(value):
    """
    Format value as Nepali Rupees.
    Usage: {{ property.price|npr }}
    """
    return format_npr(value)


@register.filter
def truncate(value, length=100):
    """
    Truncate text to specified length.
    Usage: {{ property.description|truncate:150 }}
    """
    return truncate_text(value, length)


@register.simple_tag
def npr_format(value):
    """
    Format value as Nepali Rupees (as tag).
    Usage: {% npr_format property.price %}
    """
    return format_npr(value)


@register.filter
def get_item(dictionary, key):
    """
    Get item from dictionary by key.
    Usage: {{ mydict|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def multiply(value, arg):
    """
    Multiply value by argument.
    Usage: {{ value|multiply:2 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """
    Divide value by argument.
    Usage: {{ value|divide:2 }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def percentage(value, total):
    """
    Calculate percentage.
    Usage: {{ value|percentage:total }}
    """
    try:
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    """
    Build a query string with updated parameters.
    Usage: {% query_string page=2 %} -> "page=2&existing_param=value"
    """
    request = context.get('request')
    if request is None:
        return ''
    
    # Copy current query parameters
    params = request.GET.copy()
    
    # Update with new parameters
    for key, value in kwargs.items():
        if value is None or value == '':
            params.pop(key, None)
        else:
            params[key] = value
    
    return params.urlencode()
