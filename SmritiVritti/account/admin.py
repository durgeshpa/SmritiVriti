from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import AddUserForm,UpdateUserForm

from .models import User

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType




class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('username','email','mobile_no', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('username','email','mobile_no', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)