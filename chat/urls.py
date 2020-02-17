from django.urls import path, re_path
from chat.views import index, room

urlpatterns = [
    path('index/', index, name='index'),
    re_path(r'^chat/(?P<room_name>[^/]+)/$', room, name='room'),
]
