from django.contrib import admin

from apps.company.models import Companies, CompanyUpdateRequests


# Register your models here.

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'ABN', 'company_address','created_on']
    search_fields = ['company_name', 'ABN']
    ordering = ['id', ]

class CompanyUpdateRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'company','created_on','is_approved']
    search_fields = ['company__company_name', 'company__ABN']
    ordering = ['id', ]


admin.site.register(Companies, CompaniesAdmin)
admin.site.register(CompanyUpdateRequests, CompanyUpdateRequestAdmin)
