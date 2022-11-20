from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint

from apps.company.models import Companies
from utils.options import *


class CustomerInfo(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    agency = models.ForeignKey(Companies, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=CUSTOMER_TYPE)
    customer_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_ABN = models.CharField(max_length=255, null=True, blank=True)
    sms_consent = models.CharField(max_length=30, choices=SMS_CONSENT)
    lead_status = models.CharField(max_length=50, choices=LEAD_STATUS, default='New Lead')
    updated_on = models.DateTimeField(auto_now=True)

    unique_together = ['customer', 'agency']

    def __str__(self):
        return self.customer_name
