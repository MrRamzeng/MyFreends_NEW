from django.forms import ModelForm

from chat.models import Chat
from account.models import Account
from django.contrib.auth import get_user_model
user = get_user_model()
class ChatForm(ModelForm):
    
    class Meta:
        model = Chat
        fields = ('name', 'user_list')