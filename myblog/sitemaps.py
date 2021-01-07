from .models import Post
from django.contrib.sitemaps import Sitemap

class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_post_absolute_url()