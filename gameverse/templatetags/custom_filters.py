from django import template

register = template.Library()

@register.filter
def to(value):
    try:
        value = int(value)
        return range(1, value + 1)
    except (ValueError, TypeError):
        return []
