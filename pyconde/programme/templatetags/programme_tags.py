from django import template
from django.conf import settings
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_day(event):
    day = (event.start.date() - settings.FIRST_DAY).days + 1
    return day

@register.filter
def posorder(preslist):
    return preslist.order_by("position")

from ..utils import nice_repr

@register.filter(name='timedelta')
def timedelta(value, display="long"):
    if value is None:
        return value
    return nice_repr(value, display)
