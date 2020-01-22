from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from chat.models import Message
from itertools import chain


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    
    def fetch_messages(self, data):
        room = self.room_name
        from_username = room[room.find('_') + 1:]
        to_username = room[:room.find('_')]
        sender = User.objects.get(username=from_username)
        recipient = User.objects.get(username=to_username)
        messagesFromUser = Message.objects.filter(sender=sender, recipient=recipient)
        messagesToUser = Message.objects.filter(sender=recipient, recipient=sender)
        messages = sorted(
            chain(messagesFromUser, messagesToUser),
            key=lambda instance: instance.published
        )
        message = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(message)

    def new_message(self, data):
        fromSender = data['fromSender']
        toRecipient = data['toRecipient']
        sender_user = User.objects.filter(username=fromSender)[0]
        recipient = User.objects.filter(username=toRecipient)[0]
        message = Message.objects.create(
            sender=sender_user, 
            message=data['message'],
            recipient=recipient
        )
        message = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(message)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'message': message.message,
            'published': str(message.published)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
        