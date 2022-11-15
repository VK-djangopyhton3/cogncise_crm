from django.contrib import admin

from apps.jobs.models import WorkType, Jobs, JobTransferHistory


# Register your models here.

class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_type', 'is_active']
    list_filter = ['is_active']
    search_fields = ['work_type']
    ordering = ['id', ]


class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'agent', 'work_type', 'job_status']
    list_filter = ['job_status', 'work_type']
    search_fields = ['work_type']
    ordering = ['id', ]


class JobTransferHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'agency', 'is_current_assignee']
    list_filter = ['is_current_assignee', 'agency']
    search_fields = ['job__job_status', 'job__customer__customer__name']
    ordering = ['id', ]


admin.site.register(WorkType, WorkTypeAdmin)
admin.site.register(Jobs, JobAdmin)
admin.site.register(JobTransferHistory, JobTransferHistoryAdmin)
