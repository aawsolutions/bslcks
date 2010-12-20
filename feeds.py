from django.contrib.syndication.views import Feed
from django.contrib.markup.templatetags import markup
from basic.blog.models import Post
from bslcks.bslctags.templatetags import mytags
from bslcks.bslctags.templatetags import process_flat
from basic.inlines.templatetags import inlines

from datetime import datetime

class LatestNewsFeed(Feed):
    title = "Beautiful Savior Lutheran Church Current News"
    link = "http://www.bslcks.org/news/"
    description = "10 most recent storie from the Beautiful Savior website"

    def items(self):
        return Post.objects.filter(status=2).filter(publish__lte=datetime.now()).order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        item.body = process_flat.parse_blocks(item.body)
        item.body = inlines.render_inlines(item.body)
        item.body = markup.markdown(item.body)
        return mytags.privatize(item.body)

