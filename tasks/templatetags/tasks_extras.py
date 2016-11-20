from django import template
from collections import ItemsView

register = template.Library()


@register.filter
def sort(value):
    if isinstance(value, ItemsView) or isinstance(value, list):
        return sorted(value)
    else:
        return value
