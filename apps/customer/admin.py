from django.contrib import admin

from apps.customer.models import CustomerInfo


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'lead_status', 'type', 'updated_on']
    list_filter = ['type','lead_status']
    search_fields = ['customer_name']
    ordering = ['id', ]


admin.site.register(CustomerInfo, CustomerAdmin)

