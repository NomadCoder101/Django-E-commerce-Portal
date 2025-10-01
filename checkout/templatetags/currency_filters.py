from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def currency(value, currency_code=None):
    """
    Format a value as currency with the given currency code.
    Usage: {{ value|currency:"USD" }} or {{ value|currency:currency_code }}
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return ''

    if currency_code:
        # You can extend this with more currency symbols and formatting rules
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
        }
        symbol = currency_symbols.get(currency_code, currency_code + ' ')
        return f"{symbol}{floatformat(value, 2)}"
    
    return floatformat(value, 2)