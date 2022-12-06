from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from core.abstract_models import BaseModel

class Address(BaseModel):
    building_number = models.CharField( _("building number"), max_length=100, null=True, blank=True )
    level_number = models.CharField( _("level number"), max_length=100, null=True, blank=True )
    unit_type = models.CharField( _("unit type"), max_length=100, null=True, blank=True )
    unit_number = models.CharField( _("unit number"), max_length=100, null=True, blank=True )
    lot_number = models.CharField( _("lot number"), max_length=100, null=True, blank=True )
    street_number = models.CharField( _("street number"), max_length=100, null=True, blank=True )
    street_name = models.CharField( _("street name"), max_length=100, null=True, blank=True )
    street_type = models.CharField( _("street type"), max_length=100, null=True, blank=True )
    suffix = models.CharField( _("suffix"), max_length=100, null=True, blank=True )
    suburb = models.CharField( _("suburb"), max_length=100, null=True, blank=True )
    state = models.CharField( _("state"), max_length=100)
    pincode = models.CharField( _("pincode"), max_length=10)
    purpose = models.CharField(_("purpose"), max_length=100, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.building_number} {self.street_name} {self.state} {self.pincode}"
