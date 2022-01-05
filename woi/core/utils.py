from http import HTTPStatus
from io import StringIO

import markdown

from django.http import HttpResponse
from django.template import RequestContext
from django.template.engine import Engine
from markdown import Markdown

from .md_extensions import WoiLinkExtension


def create_html(text: str) -> str:
    return markdown.markdown(
        text, extensions=[WoiLinkExtension(), 'extra', 'toc']
    )


def _unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        _unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


def unmark(text: str) -> str:
    Markdown.output_formats['plain'] = _unmark_element
    _md = Markdown(output_format='plain')
    _md.stripTopLevelTags = False
    return _md.convert(text)


def render_template(req, template_name: str, dict_: dict = None) -> str:
    engine = Engine.get_default()
    template = engine.get_template(template_name)
    d = dict_ or {}
    ctx = RequestContext(req, d)
    return template.render(ctx)


class HttpResponseCreated(HttpResponse):
    status_code = HTTPStatus.CREATED
