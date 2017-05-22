""" Filter to return items in sorted order """
from collections import ItemsView
from django import template

register = template.Library()


@register.filter
def sort(value):
    """ The filter to return the sorted order of a list """
    if isinstance(value, (ItemsView, list)):
        return sorted(value)
    return value
