from django import forms

from chat.models import MessageImage

class ImageForm(forms.ModelForm):

    class Meta:
        model = MessageImage
        fields = ('img',)
