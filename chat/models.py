from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    user_list = models.ManyToManyField(User)

    def __str__(self):
        users = ", ".join(str(user_data) for user_data in self.user_list.all())
        return str(self.name) + " {}".format(users)


class MessageSmile(models.Model):
    img = models.ImageField(upload_to='smiles/')


class MessageImage(models.Model):
    img = models.ImageField(upload_to='chat/')


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    img = models.ForeignKey(MessageImage, null=True, on_delete=models.SET_NULL)
    smile = models.ForeignKey(MessageSmile, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username