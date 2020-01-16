from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import LoginView, profile

urlpatterns = [
    path('', LoginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_profile/', profile, name='profile'),
]
