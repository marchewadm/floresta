from django import template

register = template.Library()


@register.filter
def to_dash(value):
    """Converts a whitespace to dash character"""
    return value.replace(" ", "-")
