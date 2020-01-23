from django.urls import path, re_path
from chat.views import chat

urlpatterns = [
    path('chat/', chat, name='chat'),
]
