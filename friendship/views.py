from django.contrib.auth.decorators import login_required
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

from django.shortcuts import render, get_object_or_404, redirect

from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, Follow, FriendshipRequest, Block
from account.models import Account
# from Post.models import Post

get_friendship_context_object_name = lambda: getattr(
    settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user'
)
get_friendship_context_object_list_name = lambda: getattr(
    settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users'
)


@login_required(login_url="signin")
def accounts(request):
    friends = Friend.objects.friends(request.user)
    followers = Follow.objects.followers(request.user)
    following = Follow.objects.following(request.user)
    blockers = Block.objects.blocked(request.user) # Блокирующие
    blockings = Block.objects.blocking(request.user) # Заблокированные
    friends_count = Friend.objects.filter(from_user=request.user).count()
    requests_from = Friend.objects.sent_requests(request.user) # Отпаравлены
    from_users = [
        u.from_user for u in FriendshipRequest.objects.filter(
            to_user=request.user
        )
    ]
    requests_to = FriendshipRequest.objects.filter(
        to_user=request.user, rejected__isnull=True
    ) # Получены
    to_users = [
        u.to_user for u in FriendshipRequest.objects.filter(
            from_user=request.user
        )
    ]
    users = Account.objects.exclude(
        username=request.user.username
    ).order_by("?")
    args = {
        'friends': friends, 'users': users, 'requests_from': requests_from,
        'following': following, 'followers': followers, 'blockings': blockings,
        'blockers': blockers, 'requests_to': requests_to, 'to_users': to_users,
        'friends_count': friends_count, 'from_users': from_users
    }
    return render(request, 'accounts/account_cards.html', args)


@login_required(login_url="signin")
def view_account(request, username):
    user = Account.objects.get(username=username)
    # posts = Post.objects.all().filter(user=user)
    friend_counter = Friend.objects.filter(from_user=user).count()
    follower_counter = Follow.objects.filter(followee=user).count()
    args = {
        'user': user, 'friend_counter': friend_counter,
        'follower_counter': follower_counter #, 'posts': posts
    }
    return render(request, 'accounts/account.html', args)

################################### Friends ###################################

@login_required
def friends(request, username):
    """ View the friends of a user """
    blockers = Block.objects.blocked(request.user) # Блокирующие
    blockings = Block.objects.blocking(request.user) # Заблокированные
    user = get_object_or_404(user_model, username=username)
    friends = Friend.objects.friends(user)
    followers = Follow.objects.followers(user)
    following = Follow.objects.following(request.user)
    my_friends = Friend.objects.friends(request.user)
    my_request_from_users = [
        u.from_user for u in FriendshipRequest.objects.filter(
            to_user=request.user
        )
    ]
    my_request_to_users = [
        u.to_user for u in FriendshipRequest.objects.filter(
            from_user=request.user
        )
    ]
    friend_counter = Friend.objects.filter(from_user=user).count()
    args = { 'friends': friends, 'followers': followers, 'blockings': blockings,
        'following': following, get_friendship_context_object_name(): user,
        'counter': friend_counter, 'blockers': blockers,
        'friendship_context_object_name': get_friendship_context_object_name(),
        'my_friends': my_friends, 'my_request_from_users': my_request_from_users,
        'my_request_to_users': my_request_to_users
    }
    return render(request, 'friends/friend_cards.html', args)


@login_required
def add_friend(request, username):
    other_user = Account.objects.get(username=username)
    Friend.objects.add_friend(request.user, other_user)
    return redirect('accounts')


@login_required
def cancel_friend_request(request, username):
    FriendshipRequest.objects.get(
        from_user=request.user,
        to_user=Account.objects.get(username=username)
    ).delete()
    return redirect('accounts')


@login_required
def accept_friend_request(request, username):
    other_user = Account.objects.get(username=username)
    friend_request = FriendshipRequest.objects.get(
        to_user=request.user,
        from_user=other_user
    )
    friend_request.accept()
    return redirect('accounts')


@login_required
def reject_friend_request(request, username):
    FriendshipRequest.objects.get(
        to_user=request.user,
        from_user=Account.objects.get(username=username)
    ).reject()
    Follow.objects.add_follower(Account.objects.get(username=username), request.user)
    return redirect('accounts')


@login_required
def remove_friend(request, username):
    other_user = Account.objects.get(username=username)
    Friend.objects.remove_friend(request.user, other_user)
    Follow.objects.add_follower(other_user, request.user)
    return redirect('accounts')

################################### Followers ###################################

@login_required
def followers(request, username):
    user = get_object_or_404(user_model, username=username)
    follower_counter = Follow.objects.filter(followee=user).count()
    follower_cards = Follow.objects.followers(user)
    friends = Friend.objects.friends(request.user)
    my_request_from_users = [
        u.from_user for u in FriendshipRequest.objects.filter(
            to_user=request.user
        )
    ]
    my_request_to_users = [
        u.to_user for u in FriendshipRequest.objects.filter(
            from_user=request.user
        )
    ]
    following = Follow.objects.following(request.user)
    args = {
        get_friendship_context_object_name(): user, 'following': following,
        'counter': follower_counter, 'followers': follower_cards,
        'my_request_from_users': my_request_from_users,
        'my_request_to_users': my_request_to_users, 'friends': friends
    }
    return render(request, 'followers/follower_cards.html', args)


@login_required
def add_follower(request, username):
    other_user = Account.objects.get(username=username)
    Follow.objects.add_follower(other_user, request.user)
    return redirect('view_account', other_user.username)


@login_required
def remove_follower(request, username):
    other_user = Account.objects.get(username=username)
    Follow.objects.remove_follower(other_user, request.user)
    try:
        FriendshipRequest.objects.get(
            from_user=request.user,
            to_user=other_user
        ).delete()
    except FriendshipRequest.DoesNotExist:
        pass
    return redirect('view_account', other_user.username)


@login_required
def unfollow(request, username):
    other_user = Account.objects.get(username=username)
    Follow.objects.remove_follower(request.user, other_user)
    try:
        FriendshipRequest.objects.get(
            from_user=request.user,
            to_user=other_user
        ).delete()
    except FriendshipRequest.DoesNotExist:
        pass
    return redirect('view_account', other_user.username)

################################### Block ###################################

def add_block(request, username):
    other_user = Account.objects.get(username=username)
    Block.objects.add_block(request.user, other_user)
    try:
        FriendshipRequest.objects.get(
            to_user=request.user,
            from_user=Account.objects.get(username=username)
        ).delete()
    except FriendshipRequest.DoesNotExist:
        pass
    return redirect('accounts')


def remove_block(request, username):
    Block.objects.remove_block(
        request.user, Account.objects.get(username=username)
    )
    return redirect('accounts')
