from django import template


register = template.Library()


@register.filter
def get_key(dict, key):
    return dict.get(key)


@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)
