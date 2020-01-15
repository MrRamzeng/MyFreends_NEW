from django import forms
from account.models import Account
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import capfirst
from django.utils.translation import ugettext as _

UserModel = get_user_model()

class AuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required': True, 'class': 'validate', 'type': 'email',
                'onkeyup': 'this.value = this.value.toLowerCase();',
            }
        )
    )
    password = forms.CharField(
        label=_("Password"), strip=False, min_length=8,
        widget=forms.PasswordInput(
            attrs={'required': True, 'class': 'validate', 'type': 'password'}
        ),
    )
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

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

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
