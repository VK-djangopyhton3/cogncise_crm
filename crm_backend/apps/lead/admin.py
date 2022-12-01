from django.contrib import admin
from lead.models import LeadStatus, LeadSource, Lead, LeadAddress

# class RoleAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category', 'slug']

admin.site.register(LeadStatus)
admin.site.register(LeadSource)
admin.site.register(Lead)
admin.site.register(LeadAddress)