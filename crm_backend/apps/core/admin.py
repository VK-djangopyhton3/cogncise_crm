from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as StockGroup
from django.utils.translation import gettext_lazy as _

from core.models import User, Group, Role, Address
from core.settings import CUSER_SETTINGS


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # add_form_template = 'admin/core/core/add_form.html'
    fieldsets = (
        (None, {'fields': ('username', 'role', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_organization', 'is_customer', 'is_cogncise')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'email', 'password1', 'password2', 'is_organization', 'is_customer', 'is_cogncise' ),
        }),
    )
    # form = UserChangeForm
    # add_form = UserCreationForm
    list_display = ['username', 'first_name', 'email', 'is_active', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['email', 'username']



if CUSER_SETTINGS['register_proxy_auth_group_model']:
    admin.site.unregister(StockGroup)

    @admin.register(Group)
    class GroupAdmin(BaseGroupAdmin):
        pass


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']

admin.site.register(Role, RoleAdmin)
admin.site.register(Address)
