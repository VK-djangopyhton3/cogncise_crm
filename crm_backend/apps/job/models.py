from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from core.abstract_models import BasicInformation
from core.models import Address

class Job(BasicInformation):
    title = models.CharField( _("title"), max_length=100)
    addresses = GenericRelation(Address, related_query_name='job')
    
    def __str__(self):
        return f"{self.title}"

    @property
    def business_address(self):
        return self.addresses.filter(purpose='business').last()

    @property
    def property_address(self):
        return self.addresses.filter(purpose='property').last()
