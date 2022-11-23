from django.contrib import admin

from apps.appointments.models import AppointmentType, Appointment, AppointmentComments

# Register your models here.

admin.site.register(AppointmentType)
admin.site.register(Appointment)
admin.site.register(AppointmentComments)
