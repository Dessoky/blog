from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.simple_tag(name="my_tag")
def total_posts():
    """
    a simple template tag that returns the number of posts published so far
    if name attribute is provided the tag will be named by that
    if not provided the tag will be named by the function name total_posts
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    Inclusion tags returns a dictionary of context to use in the provided template
    the count argument can be used next to the tag like: {% show_latest_posts 3 %}
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return{'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
