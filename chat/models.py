from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=50)
    user_list = models.ManyToManyField(User, related_name='recipients')


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username