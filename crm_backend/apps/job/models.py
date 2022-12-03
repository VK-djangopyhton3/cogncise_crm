from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from shared.models import Address
from company.models import Company
from core.abstract_models import BasicInformation

class Job(BasicInformation):
    title = models.CharField( _("title"),  max_length=100)
    addresses = GenericRelation(Address,   related_query_name='job')
    company   = models.ForeignKey(Company, related_name="job_company", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}"

    @property
    def business_address(self):
        return self.addresses.filter(purpose='business').last()

    @property
    def property_address(self):
        return self.addresses.filter(purpose='property').last()
