from django.contrib import admin

from lead.models import LeadStatus, LeadSource, Lead

admin.site.register(LeadStatus)
admin.site.register(LeadSource)
admin.site.register(Lead)
