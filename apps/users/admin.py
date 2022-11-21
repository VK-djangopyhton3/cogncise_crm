from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User, UserRoles, StaffAssociate


# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password', 'last_login', 'is_verified',)}),
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
                'fields': ('phone', 'password1', 'password2', 'is_staff', 'is_superuser')
            }
        ),
    )

    list_display = ('id', 'phone', 'email', 'is_active', 'is_verified', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'email')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions',)


class UserRolesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'company', 'role']
    list_filter = ['role']
    search_fields = ['company__company_name',]
    ordering = ['id', ]


class StaffAssociateAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'company']
    list_filter = ['company']
    search_fields = ['company__company_name']
    ordering = ['id', ]


admin.site.register(User, UserAdmin)
admin.site.register(UserRoles, UserRolesAdmin)
admin.site.register(StaffAssociate, StaffAssociateAdmin)
