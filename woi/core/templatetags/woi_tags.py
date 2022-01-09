from django import template
from django.conf import settings
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


@register.inclusion_tag('core/ganalytics.html')
def google_analytics(options=''):
    gtags_id = getattr(settings, 'WOI_GOOGLE_ANALYTICS_ID', '').strip()
    return {'gtags_id': gtags_id}
