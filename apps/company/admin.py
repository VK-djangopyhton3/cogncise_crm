from django.contrib import admin

from apps.company.models import Companies


# Register your models here.

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'ABN', 'company_address']
    search_fields = ['company_name', 'ABN']
    ordering = ['id', ]


admin.site.register(Companies, CompaniesAdmin)
