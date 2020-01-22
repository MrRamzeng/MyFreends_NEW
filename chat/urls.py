from django.urls import path, re_path
from chat.views import chat, chatroom

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('<str:User>_<str:username>/', chatroom, name='chatroom'),
]
