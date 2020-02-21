from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from json import dumps
from account.models import Account
from chat.models import Chat, MessageImage, MessageSmile
from chat.forms import ChatForm

@login_required(login_url='signin')
def index(request):
    return render(request, 'chat/index.html', {})


@login_required(login_url='signin')
def room(request, id):
    accounts = Account.objects.all()
    chats = Chat.objects.filter(user_list=request.user)
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room', form.save().id)
    else:
        form = ChatForm()
    return render(request, 'chat/room.html', {
        'chat_id': mark_safe(dumps(id)),
        'id': mark_safe(dumps(request.user.id)),
        'chats': chats, 'accounts': accounts, 'form': form
    })


@login_required(login_url='signin')
def upload_image(request):
    if request.method == 'POST' and request.FILES['img']:
        image = MessageImage(img=request.FILES['img'])
        image.save()
        return JsonResponse({'success': True, 'id': image.id})
    return JsonResponse({'success': False, 'message': 'no file'})


@login_required(login_url='signin')
def create_chat(request):
    if request.method == 'post':
        chat = Chat(name=request['name'], user_list=request['user_list'])
        chat.save()
        return JsonResponse({'success': True, 'id': chat.id})
    return JsonResponse({'success': False, 'message': 'no data'})