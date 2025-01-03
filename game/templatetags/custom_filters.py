from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter
def avatar_url(user):
    if user.avatar:
        return user.avatar.url
    return static('default-avatar.png')