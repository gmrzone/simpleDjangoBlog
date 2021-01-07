from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag(name='post_count')
def post_count():
    count = Post.published.count()
    return count

@register.inclusion_tag('myblog/latest_post.html')
def show_latest_post(count=5):
    posts = Post.published.all()[:count]
    context = {'latest_post': posts}
    return context

@register.simple_tag
def post_with_most_comments(count=3):
    posts = Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]
    return posts

@register.filter(name='markdown')
def markdown_format(value):
    return mark_safe(markdown.markdown(value))
