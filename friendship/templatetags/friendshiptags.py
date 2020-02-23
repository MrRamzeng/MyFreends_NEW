from django import template

from friendship.models import Friend, Follow, FriendshipRequest, Block

register = template.Library()


@register.simple_tag(takes_context=True)
def get_by_name(context, name):
    """Tag to lookup a variable in the current context."""
    return context[name]
    

@register.inclusion_tag('templatetags/friends.html')
def friends(user):
    """
    Simple tag to grab all friends
    """
    return {'friends': Friend.objects.friends(user)}
