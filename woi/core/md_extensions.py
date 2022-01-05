import xml.etree.ElementTree as etree

from django.urls import reverse
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


LINK_PATTERN = r':woi-(?P<type>article|info):(?P<slug>.+?)(?P<text>:.*?)?:'
_cache = {}


class WoiLinkInlineProcessor(InlineProcessor):

    def _handle_article(self, slug):
        ctag = f'article__{slug}'
        if ctag in _cache:
            return _cache[ctag]
        from .models import Post
        try:
            post = Post.objects.get(slug=slug)
            link = reverse('core:article', args=(slug,))
            text = post.title
        except Post.DoesNotExist:
            link = '/'
            text = f'Post: {slug} not found'
        _cache[ctag] = (link, text)
        return link, text

    def _handle_info(self, ident):
        ctag = f'info__{ident}'
        if ctag in _cache:
            return _cache[ctag]
        from .models import SiteInfo
        try:
            info = SiteInfo.objects.get(ident=ident)
            link = reverse('core:info', args=(ident,))
            text = info.name
        except SiteInfo.DoesNotExist:
            link = '/'
            text = f'SiteInfo: {ident} not found'
        _cache[ctag] = (link, text)
        return link, text

    def handleMatch(self, m, data):
        if m.group('type') == 'article':
            link, text = self._handle_article(m.group('slug'))
        else:
            link, text = self._handle_info(m.group('slug'))
        if 'text' in m.groupdict() and m.group('text') and link != '/':
            text = m.group('text').strip(' :')
        el = etree.Element('a')
        el.text = text
        el.set('href', link)
        return el, m.start(0), m.end(0)


class WoiLinkExtension(Extension):

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            WoiLinkInlineProcessor(LINK_PATTERN, md), 'woilinks', 150
        )
