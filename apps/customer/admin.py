from django.contrib import admin

from apps.customer.models import CustomerInfo


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'updated_on']
    list_filter = ['type']
    search_fields = ['customer__name']
    ordering = ['id', ]


admin.site.register(CustomerInfo, CustomerAdmin)

