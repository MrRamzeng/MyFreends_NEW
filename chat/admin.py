from django.contrib import admin
from chat.models import Message, MessageSmile

admin.site.register(MessageSmile)
admin.site.register(Message)
