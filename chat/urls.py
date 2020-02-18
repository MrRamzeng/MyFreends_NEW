from django.urls import path, re_path
from chat.views import index, room

urlpatterns = [
    path('index/', index, name='index'),
    path('chat/<int:id>/', room, name='room'),
]
