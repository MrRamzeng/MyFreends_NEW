from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json

from chat.models import Chat
from chat.forms import ChatForm

def index(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            print(name)
            form.save()
            JsonResponse({'success': True, 'name': name})
    else:
        form = ChatForm()
    return render(request, 'chat/index.html', {'form': form})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })