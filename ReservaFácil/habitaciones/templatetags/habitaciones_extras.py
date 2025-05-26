from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica value por arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency_format(value):
    """Formatea un número como moneda colombiana"""
    try:
        return f"${float(value):,.0f} COP"
    except (ValueError, TypeError):
        return "$0 COP" 