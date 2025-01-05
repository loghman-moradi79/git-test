from lib2to3.fixes.fix_input import context

from django import template
from django.db.models import Count, Max
from ..models import Post, Comment, User
from markdown import markdown
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag()
def number_of_posts():
    return Post.published.count()


@register.simple_tag()
def number_of_comment():
    return Comment.objects.count()


@register.simple_tag()
def time_of_last_post():
    return Post.published.last().publish


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=3):
    l_post = Post.published.order_by('-publish')[:count]
    context = {
        'l_post': l_post,
    }
    return context


@register.simple_tag()
def most_popular_post(count=2):
    return Post.published.annotate(count=Count('comments')).order_by('-count')[:count]


@register.filter('markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


word_bad_fa = {'احمقی', 'عوضی', 'بیشعوری'}


@register.filter(name='censor')
def word_censor(text):
    for word in word_bad_fa:
        if word in text:
            text = text.replace(word, '*' * len(word))
    return text


@register.simple_tag()
def active_users(count=3):
    return User.objects.annotate(max=Count('user_posts')).order_by('-max')[:count]







