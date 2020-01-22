from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth import get_user_model
from chat.models import Message
from django.utils.safestring import mark_safe
import json

User = get_user_model()
User = User.username

def chat(request):
    users = Account.objects.exclude(username=request.user.username)
    userCounter = users.count()
    return render(
        request, 'chat/chat.html', 
        {
            'users': users, 'u_counter': userCounter
        }
    )

def chatroom(request, User, username):
    users = Account.objects.exclude(username=request.user.username)
    user = Account.objects.get(username=username)
    fromSenderLastMessage = Message.objects.filter(sender=request.user, recipient=user).last()
    toRecipientLastMessage = Message.objects.filter(recipient=request.user, sender=user).last()
    url = request.user.username + '_' + user.username
    url2 = user.username + '_' + request.user.username
    return render(
        request, 'chat/chatroom.html', 
        {
            'users': users, 'user': user,
            'room_name_json': mark_safe(json.dumps(url)),
            'room_name_json2': mark_safe(json.dumps(url2)),
            'from_last_message': fromSenderLastMessage, 'to_last_message': toRecipientLastMessage,
            'first_name': mark_safe(json.dumps(request.user.first_name)),
        }
    )
