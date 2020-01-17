from django.contrib import admin
from account.models import Account
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

class CustomAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'is_staff', 'is_active')
    list_filter = ('username', 'is_staff')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff')}
        ),
    )
    search_fields = ('username',)
    list_per_page = 50

admin.site.unregister(Group)
admin.site.register(Account, CustomAdmin)
