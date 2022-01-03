from django.conf import settings
from django.urls import reverse

from .models import Extension


def add_woi_variables(req):
    q = Extension.objects.filter(active=True).exclude(js_file__in=['', None])
    woi_js = {
        'left_url': req.build_absolute_uri(
            reverse('core:extensions', args=('left',))
        ),
        'right_url': req.build_absolute_uri(
            reverse('core:extensions', args=('right',))
        ),
        'save_comment_url': req.build_absolute_uri(
            reverse('core:save-comment')
        ),
    }
    return {
        'woi_title': getattr(settings, 'WOI_TITLE', ''),
        'woi_subtitle': getattr(settings, 'WOI_SUBTITLE', ''),
        'woi_footer': getattr(settings, 'WOI_FOOTER', True),
        'woi_content_license': settings.WOI_CONTENT_LICENSE,
        'woi_ext_js': bool(q.count()),
        'woi_ip': req.META.get('REMOTE_ADDR', ''),
        'woi_js': woi_js,
    }
