from django.db import models

from apps.company.models import Companies
from apps.customer.models import CustomerInfo
from apps.properties.models import Property
from crm_backend import settings
from utils.options import LEAD_STATUS


# Create your models here.

class WorkType(models.Model):
    work_type = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.work_type


class Jobs(models.Model):
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    property_address = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.customer.name


class JobTransferHistory(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    agency = models.ForeignKey(Companies, on_delete=models.CASCADE)
    transfer_count = models.IntegerField(default=0)
    assigned_on = models.DateTimeField(auto_now=True)
    is_current_assignee = models.BooleanField(default=True)

    def __int__(self):
        return self.job.id
