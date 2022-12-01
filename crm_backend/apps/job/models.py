from django.db import models

from django.utils.translation import gettext_lazy as _
# from core.models import BaseModel,, 
from core.abstract_models import BasicInformation, BaseModel
from common.app_utils import profile_unique_upload
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

# Create your models here.

class Address(BaseModel):
    building_number = models.CharField( _("Building number"), max_length=100, null=True, blank=True )
    level_number = models.CharField( _("Level number"), max_length=100, null=True, blank=True )
    unit_type = models.CharField( _("unit type"), max_length=100, null=True, blank=True )
    unit_number = models.CharField( _("unit number"), max_length=100, null=True, blank=True )
    lot_number = models.CharField( _("lot number"), max_length=100, null=True, blank=True )
    street_number = models.CharField( _("street number"), max_length=100, null=True, blank=True )
    street_name = models.CharField( _("street name"), max_length=100, null=True, blank=True )
    street_type = models.CharField( _("street type"), max_length=100, null=True, blank=True )
    suffix = models.CharField( _("suffix"), max_length=100, null=True, blank=True )
    suburb = models.CharField( _("suburb"), max_length=100, null=True, blank=True )
    state = models.CharField( _("State"), max_length=100, null=True, blank=True )
    pincode = models.CharField( _("pincode"), max_length=10 )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Job(BasicInformation):
    # ref_id = 
    # customer_id = 
    # sms_consent_type = 
    address = GenericRelation(Address, related_query_name="job")
    # property_address = GenericRelation(Address, related_query_name="property_address")
