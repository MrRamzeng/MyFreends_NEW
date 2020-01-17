from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from account.views import LoginView, signup, activate, signup_confirm, profile

urlpatterns = [
    path('signin/', LoginView.as_view(), name='signin'),
    path('signup/', signup, name='signup'),
    re_path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/"
        "(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        activate, name="activate"
    ),
    path('signup_confirm/', signup_confirm, name='signup_confirm'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('my_profile/', profile, name='profile'),
]
