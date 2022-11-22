from django.contrib import admin

from apps.customer.models import CustomerInfo


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'lead_status',  'updated_on']
    list_filter = ['lead_status']
    search_fields = ['customer_name']
    ordering = ['id', ]


admin.site.register(CustomerInfo, CustomerAdmin)

