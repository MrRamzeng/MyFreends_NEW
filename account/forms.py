from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.text import capfirst
from django.utils.translation import ugettext as _

from account.models import Account

UserModel = get_user_model()

class SigninForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'signin_email', 'class': 'validate', 'type': 'email',
                'name': 'signin_email', 'required': True,
                'onkeyup': 'this.value = this.value.toLowerCase();',
            }
        )
    )
    password = forms.CharField(
        label=_("Password"), strip=False, min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'id': 'signin_password', 'class': 'validate',
                'type': 'password', 'name': 'signin_password',
                'required': True,
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD
        )
        self.fields['username'].max_length = (
            self.username_field.max_length or 254
        )
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(
                self.username_field.verbose_name
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label=_('Password'), min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'id': 'signup_password1', 'class': 'validate', 
                'type': 'password', 'name': 'signup_password1',
                'required': True
            }
        )
    )
    password2 = forms.CharField(
        label=_('Repeat please the password'), min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'id': 'signup_password2', 'class': 'validate',
                'type': 'password', 'name': 'signup_password2',
                'required': True
            }
        )
    )

    class Meta:
        model = Account
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password1', 'password2'
        )
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'required': True, 'class': 'validate', 'type': 'email',
                    'onkeyup': 'this.value = this.value.toLowerCase();',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'id': 'signup_username', 'class': 'validate',
                    'type': 'text', 'name': 'signup_username',
                    'required': True
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'required': True, 'class': 'validate',
                    'pattern': '^[A-Za-zА-Яа-я]+$'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'required': True, 'class': 'validate',
                    'pattern': '^[A-Za-zА-Яа-я]+$'
                }
            )
        }
