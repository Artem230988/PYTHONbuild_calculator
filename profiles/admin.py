from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'second_name',
                                         'last_name', 'email', 'phone',
                                         'photo', 'current_employee')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff',
                       'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
