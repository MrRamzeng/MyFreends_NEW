from django import forms 
from chat.models import Chat
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe
from account.models import Account
from django.template.loader import render_to_string


class ChatForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ('name', 'user_list')
        widgets = {
            'user_list': forms.CheckboxSelectMultiple()
        }
