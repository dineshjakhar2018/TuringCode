# custom_filters.py

from django import template
register = template.Library()

@register.filter
def format_seconds(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

@register.filter
def append_to_list(list, item):
    new_list = list.copy()
    new_list.append(item)
    return new_list

@register.filter
def subtract(value, arg):
    return value - arg
