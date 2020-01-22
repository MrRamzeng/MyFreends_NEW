from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models import Account

class CustomAdmin(UserAdmin):
    model = Account
    list_display = ('username', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'photo', 'is_staff', 'is_active', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'is_staff')}
        ),
    )
    search_fields = ('email',)
    list_per_page = 50

admin.site.unregister(Group)
admin.site.register(Account, CustomAdmin)