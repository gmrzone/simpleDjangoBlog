from .models import Post
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars
from django.urls import reverse_lazy

class PostFeed(Feed):
    title = "MyBlog Latest Feed"
    link = ""
    description = 'Latest Post From Our Blog'

    def items(self):
        return Post.published.all().order_by('-publish')[:10]

    def item_link(self, item):
        return reverse_lazy('post_details', args=[item.publish.year, item.publish.month, item.publish.day, item.slug])

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars(item.body, 25)