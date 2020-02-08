from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from account.models import Account
from chat.models import Message, MessageImage
from chat.forms import ImageForm

User = get_user_model()
User = User.username


@login_required(login_url='signin')
def chat(request):
    users = Account.objects.exclude(username=request.user.username)
    lastMessageFromSender = Message.objects.filter(sender=request.user).last()
    lastMessageFromRecipient = Message.objects.filter(
        recipient=request.user
    ).last()
    form = ImageForm(request.FILES)
    return render(
        request, 'chat/chat.html', 
        {
            'users': users, 'lastMessageFromSender': lastMessageFromSender,
            'lastMessageFromRecipient': lastMessageFromRecipient, 'form': form,
        }
    )

@login_required(login_url='signin')
def upload_image(request):
    if request.method == 'POST' and request.FILES['img']:

        image = MessageImage(img=request.FILES['img'])
        image.save()
        return JsonResponse({'success': True, 'id': image.id})

    return JsonResponse({'success': False, 'message': 'no file'})
