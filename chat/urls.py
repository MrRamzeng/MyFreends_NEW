from django.urls import path, re_path
from chat.views import index, room, upload_image, create_chat

urlpatterns = [
    path('index/', index, name='index'),
    path('chat/<int:id>/', room, name='room'),
    path('chat/up_image/', upload_image, name='upload'),
    path('chat/create/', create_chat, name='create_chat'),
]
