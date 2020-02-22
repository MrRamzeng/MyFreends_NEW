from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from json import dumps

from account.models import Account
from chat.models import Chat, MessageImage, MessageSmile
from chat.forms import ChatForm


@login_required(login_url='signin')
def chat(request):
    accounts = Account.objects.all()
    chats = Chat.objects.filter(user_list=request.user)
    smiles = MessageSmile.objects.all()
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')
    else:
        form = ChatForm()
    return render(request, 'chat/chat.html', {
        'chats': chats, 'accounts': accounts, 'form': form, 'smiles': smiles
    })


@login_required(login_url='signin')
def upload_image(request):
    if request.method == 'POST' and request.FILES['img']:
        image = MessageImage(img=request.FILES['img'])
        image.save()
        return JsonResponse({'success': True, 'id': image.id})
    return JsonResponse({'success': False, 'message': 'no file'})
