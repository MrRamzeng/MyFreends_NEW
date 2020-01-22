from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from MyFreends import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('password/', include('password_reset.urls')),
    path('', include('account.urls')),
    path('', RedirectView.as_view(url='my_profile')),
    # path('', include('friendship.urls')),
    path('', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
