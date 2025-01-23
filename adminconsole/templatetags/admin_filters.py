from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.safestring import mark_safe
from django import template
import pdb
from datetime import datetime
register = template.Library()


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=1, on_ends=1):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, on_each_side=1, on_ends=1)


@register.filter
def times(number):
    return range(number)


@register.filter(name='camel_case')
def camel_case(value):
    """Converts a string to camelCase."""
    words = value.split()
    if not words:
        return value
    # Capitalize each word except the first one
    camel_cased = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return camel_cased



@register.filter(name='capitalize')
def capitalize(value):
    """Capitalizes the first letter of each word in a string."""
    if not isinstance(value, str):
        return value
    return ' '.join(word.capitalize() for word in value.split())



@register.filter
def format_order(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value  #
    
    
@register.filter
def format_price(value):
    """
    Formats a number to two decimal places.
    """
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return "0.00"  # Return a default value if the input i
    

@register.filter
def range_filter(value):
    return range(value)

