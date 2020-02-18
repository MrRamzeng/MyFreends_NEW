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
            id = form.cleaned_data.get('id')
            print(name)
            form.save()
            JsonResponse({'success': True, 'id': id})
    else:
        form = ChatForm()
    return render(request, 'chat/index.html', {'form': form})

@login_required
def room(request, id):
    return render(request, 'chat/room.html', {
        'room_id': mark_safe(json.dumps(id)),
        'username': mark_safe(json.dumps(request.user.username)),
    })