from django.contrib import admin


from apps.jobs.models import WorkType, Jobs

# Register your models here.

admin.site.register(WorkType)
admin.site.register(Jobs)
