import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from account.models import Account
from chat.models import Message
User = get_user_model()
User = User.username


@login_required(login_url='signin')
def chat(request):
    users = Account.objects.exclude(username=request.user.username)
    lastMessageFromSender = Message.objects.filter(sender=request.user).last()
    lastMessageFromRecipient = Message.objects.filter(
        recipient=request.user
    ).last()
    return render(
        request, 'chat/chat.html', 
        {
            'users': users, 'lastMessageFromSender': lastMessageFromSender,
            'lastMessageFromRecipient': lastMessageFromRecipient,
        }
    )
