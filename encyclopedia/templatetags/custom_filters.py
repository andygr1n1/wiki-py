from django import template

register = template.Library()

@register.filter
def sort(value):
    return sorted(value, key=str.lower)