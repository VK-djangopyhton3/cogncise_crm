from django.contrib import admin
from appointment.models import WorkType, Appointment, AppointmentStatus
# Register your models here.
admin.site.register(WorkType)
admin.site.register(Appointment)
admin.site.register(AppointmentStatus)