from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import LoginView, profile

urlpatterns = [
    path('auth/', LoginView.as_view(), name='auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', profile, name='profile'),
]
