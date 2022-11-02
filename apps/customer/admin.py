from django.contrib import admin

from apps.customer.models import CustomerInfo


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'created_by', 'agency', 'created_on', 'updated_on']
    list_filter = ['type', 'agency']
    search_fields = ['agency__company_name', 'created_by__name', 'customer']
    ordering = ['id', 'created_on']


admin.site.register(CustomerInfo, CustomerAdmin)
# admin.site.register(CustomerInfo)
