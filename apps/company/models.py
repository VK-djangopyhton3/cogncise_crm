from django.conf import settings
from django.db import models



# Create your models here.
class Companies(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    company_address = models.CharField(max_length=255)
    ABN = models.CharField(max_length=255, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.id


class CompanyUpdateRequests(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # company fields
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    ABN = models.CharField(max_length=255, null=True, blank=True)
    # approval status
    is_approved = models.BooleanField(default=None,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    remarks = models.TextField()

    def __str__(self):
        return self.company.company_name
