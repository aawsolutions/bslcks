from django.contrib.syndication.views import Feed

from basic.blog.models import Post
from bslcks.bslctags.templatetags import mytags

class LatestNewsFeed(Feed):
    title = "Beautiful Savior Lutheran Church Current News"
    link = "/news/"
    description = "10 most recent storie from the Beautiful Savior website"

    def items(self):
        return Post.objects.filter(status=2).order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return mytags.privatize(item.body)[:200]

