from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class WoiRssNewsFeed(Feed):
    title = settings.WOI_TITLE or 'News Feed'
    link = '/feeds/'
    description = settings.WOI_SUBTITLE or 'Updates'

    def items(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).order_by('-updated')

    def item_title(self, item) -> str:
        return item.title

    def item_description(self, item) -> str:
        return item.get_plaintext(160)


class WoiAtomNewsFeed(WoiRssNewsFeed):
    feed_type = Atom1Feed
    subtitle = WoiRssNewsFeed.description
