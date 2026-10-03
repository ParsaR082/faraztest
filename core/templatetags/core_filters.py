from django import template

register = template.Library()

@register.filter
def splitlines(value):
    """Split a string by newlines."""
    if value:
        return value.splitlines()
    return []


_PERSIAN = '۰۱۲۳۴۵۶۷۸۹'


@register.filter
def persian_num(value):
    text = str(value)
    return ''.join(_PERSIAN[int(ch)] if ch.isdigit() else ch for ch in text)
