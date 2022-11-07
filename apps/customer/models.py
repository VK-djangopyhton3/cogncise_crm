from django.conf import settings
from django.db import models

from apps.company.models import Companies
from utils.options import *


class CustomerInfo(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer',
                                    null=False, blank=False)
    type = models.CharField(max_length=30, choices=CUSTOMER_TYPE)
    sms_consent = models.CharField(max_length=30, choices=SMS_CONSENT)
    updated_on = models.DateTimeField(auto_now=True)
