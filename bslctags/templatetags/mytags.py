from django import template
from basic.bookmarks.models import Bookmark
from basic.blog.models import Post
from photologue.models import Photo
from datetime import datetime
import re

register = template.Library()
#Load Bookmarks
class BookmarkNode(template.Node):
    def __init__(self, fetch_string):
        self.fetch_string = fetch_string
    def render(self, context):
        context[self.fetch_string] = Bookmark.objects.filter(tags__icontains=self.fetch_string)
        return '' 

@register.tag(name="fetch_bookmarks")
def do_fetch_bookmarks(parser, token):
    try:
        tag_name, fetch_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (fetch_string[0] == fetch_string[-1] and fetch_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return BookmarkNode(fetch_string[1:-1])

#Get a Photo URL
class PhotoUrlNode(template.Node):
    def __init__(self, fetch_string):
        self.fetch_string = fetch_string
    def render(self, context):
        p = Photo.objects.get(title_slug=self.fetch_string)
        return p.image.url

@register.tag(name='fetch_image_url')
def do_fetch_img_url(parser, token):
    try:
        tag_name, fetch_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (fetch_string[0] == fetch_string[-1] and fetch_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return PhotoUrlNode(fetch_string[1:-1])

#URLIFY text
urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')
@register.filter('urlify_markdown')
def urlify_markdown(value):
    value = urlfinder.sub(r'<\1>', value)
    return urlfinder2.sub(r' <\1>', value)


@register.filter('truncatechars')
def truncatechars(value, arg):
    return value[0:arg] + '...'

@register.filter('privatize')
def privatize(value):
    phonePattern = re.compile(r'''
                # don't match beginning of string, number can start anywhere
        (\d{3})     # trunk is 3 digits (e.g. '555')
        \D*         # optional separator
        (\d{4})     # rest of number is 4 digits (e.g. '1212')
        ''', re.VERBOSE)

    emailPattern = re.compile(r'''
        [\w.-]
        +@
        [\w.-]
        +
        ''', re.VERBOSE)

    phonerepl = r'[login to view #]'
    emailrepl = r'[login to view email]'

    value = re.sub(phonePattern, phonerepl, value)
    return re.sub(emailPattern, emailrepl, value)

#Load x number of blog post objects
class PostNode(template.Node):
    def __init__(self, fetch_string):
        self.fetch_string = fetch_string
    def render(self, context):
        if self.fetch_string == 'Emergency':
            try:
                context['emergency'] = Post.objects.filter(publish__lte=datetime.now()).filter(status=2).filter(categories__slug='emergency-notification').order_by('-publish')[0]
            except:
                temp = ''
        else:
            context['posts'] = Post.objects.filter(publish__lte=datetime.now()).filter(categories__slug='front-page').filter(status=2).exclude(categories__slug='emergency-notification').order_by('-publish')[0:self.fetch_string]
        return ''

@register.tag(name="fetch_posts")
def do_fetch_posts(parser, token):
    try:
        tag_name, fetch_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (fetch_string[0] == fetch_string[-1] and fetch_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return PostNode(fetch_string[1:-1])

