from django import template
from django.urls import resolve, Resolver404

register = template.Library()

@register.simple_tag
def active_nav(request, url_name):
    try:
        match = resolve(request.path_info)
        if match.url_name == url_name:
            return 'active'
    except Resolver404:
        pass
    return ''