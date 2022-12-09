from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from shared.models import Address
from company.models import Company, CompanyStatus

class AddressInline(GenericStackedInline):
    model = Address
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    inlines = [AddressInline]

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyStatus)
