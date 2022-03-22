from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

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
    """
    Returning the top 5 (by default) most commented posts
    annotate function adds a note beside each Post object using total_comments variable
    to calculate each post's comments, then ordering them by that new column added called total_comments disassending 
    then by the end of that Query set we add [:count] which is a list slicer slicing the returned list to the count of 5 that is a default value
    and can be changed by calling this tag in the template by {% get_most_commented_posts 3 %} which is no passing the argument of count = 3
    """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown((text)))
