
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from shared.models import Address

from lead.models import LeadStatus, LeadSource, Lead

class AddressInline(GenericStackedInline):
    model = Address
    extra = 1

class LeadAdmin(admin.ModelAdmin):
    inlines = [AddressInline]


admin.site.register(LeadStatus)
admin.site.register(LeadSource)
admin.site.register(Lead, LeadAdmin)




