from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import CrmUser


# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password', 'name', 'last_login', 'is_verified',)}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('phone', 'name', 'password1', 'password2')
            }
        ),
    )

    list_display = ('id', 'phone', 'name', 'is_active', 'is_verified', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'name')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CrmUser, UserAdmin)
