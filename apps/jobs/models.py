from django.db import models
from apps.company.models import Companies
from apps.customer.models import CustomerInfo
from apps.properties.models import Property
from apps.users.models import UserRoles
from utils.options import LEAD_STATUS, JOB_STATUS

# Create your models here.

class WorkType(models.Model):
    work_type = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.work_type


class Jobs(models.Model):
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    property_address = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    job_status = models.CharField(max_length=50, choices=JOB_STATUS, default='New Lead')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.customer_name





    