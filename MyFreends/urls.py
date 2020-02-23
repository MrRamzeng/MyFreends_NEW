from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from MyFreends import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', RedirectView.as_view(url='my_profile')),
    path('', include('chat.urls')),
    path('', include('friendship.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
