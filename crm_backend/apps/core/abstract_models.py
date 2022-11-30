from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class BaseModel(models.Model):
    # uuid = models.UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    is_deleted = models.BooleanField( _('is_deleted'), default=False, help_text=_('Designates whether this user should be treated as delete user. '),)

    class Meta:
        abstract = True


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

    class Meta:
        abstract = True


class BasicInformation(BaseModel):
    first_name = models.CharField( _("first name"), max_length=30, null=True, blank=True )
    last_name = models.CharField( _("last name"), max_length=30, null=True, blank=True )
    email = models.EmailField( _("Email address"), null=True, blank=False )
    mobile_number = PhoneNumberField( _('mobile number'), blank=True, null=True )

    class Meta:
        abstract = True