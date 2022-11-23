from django.db import models

from apps.properties.models import Property
from apps.users.models import UserRoles
from utils.options import APPOINTMENT_STATUS


# Create your models here.
class AppointmentType(models.Model):
    type_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name


class Appointment(models.Model):
    appointment_type = models.ForeignKey(AppointmentType, on_delete=models.CASCADE)
    property_location = models.ForeignKey(Property, on_delete=models.CASCADE)
    appointment_status = models.CharField(max_length=255, choices=APPOINTMENT_STATUS)
    field_worker = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.appointment_type.type_name
class AppointmentComments(models.Model):
    appointment = models.ForeignKey(AppointmentType, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    comments = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.commented_by.name
