from django.contrib import admin
from appointment.models import WorkType, Appointment, ScheduleAppointment
# Register your models here.
admin.site.register(WorkType)
admin.site.register(ScheduleAppointment)
admin.site.register(Appointment)