from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def permalink(context, view_name, *args, **kw):
    try:
        url = context['request'].build_absolute_uri(
            reverse(view_name, args=args, kwargs=kw)
        )
    except KeyError:
        url = 'Error: No context available'
    return url
