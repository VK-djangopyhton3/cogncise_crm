from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from shared.models import Address
from job.models import Job

# Register your models here.

class AddressInline(GenericStackedInline):
    model = Address
    extra = 1

class JobAdmin(admin.ModelAdmin):
    inlines = [AddressInline]


admin.site.register(Job, JobAdmin)


