try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url
from friendship.views import (
    accounts, view_account, friends, add_friend, cancel_friend_request,
    accept_friend_request, reject_friend_request, remove_friend, followers,
    add_follower, remove_follower, unfollow, add_block, remove_block
)

urlpatterns = [
    url(r"^accounts/$", accounts, name="accounts"),
    url(
        r"^accounts/(?P<username>.+)/$",
        view_account, name="view_account"
    ),
    url(
        r'^(?P<username>.+)/friend_cards/$',
        friends, name='friends',
    ),
    url(
        r"^add_friend/(?P<username>.+)/$",
        add_friend, name="add_friend"
    ),
    url(
        r"^cancel_friend_request/(?P<username>.+)/$",
        cancel_friend_request, name="cancel_friend_request"
    ),
    url(
        r"^accept_friend_request/(?P<username>.+)/$",
        accept_friend_request, name="accept_friend_request"
    ),
    url(
        r"^reject_friend_request/(?P<username>.+)/$",
        reject_friend_request, name="reject_friend_request"
    ),
    url(
        r"^remove_friend/(?P<username>.+)/$",
        remove_friend, name="remove_friend"
    ),
    url(
        r"(?P<username>.+)/followers/$",
        followers, name="followers"
    ),
    url(
        r"^add_follower/(?P<username>.+)/$",
        add_follower, name="add_follower"
    ),
    url(
        r"^remove_follower/(?P<username>.+)/$",
        remove_follower, name="remove_follower"
    ),
    url(
        r"^unfollow/(?P<username>.+)/$",
        unfollow, name="unfollow"
    ),
    url(
        r"^add_block/(?P<username>.+)/$",
        add_block, name="add_block"
    ),
    url(
        r"^remove_block/(?P<username>.+)/$",
        remove_block, name="remove_block"
    )
]
