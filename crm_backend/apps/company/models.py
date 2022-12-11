from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from phonenumber_field.modelfields import PhoneNumberField

from core.abstract_models import BaseModel
from common.app_utils import logo_media_upload
from shared.models import Address

User = get_user_model()

class CompanyStatus(BaseModel):
    title = models.CharField(_("Company status"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Company Status")
        verbose_name_plural = _("Company Status")
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Company(BaseModel):
    name          = models.CharField( _("name"), max_length=30)
    abn           = models.CharField( _("ABN"),  max_length=30, unique=True)
    email         = models.EmailField(_('email address'), null=True, blank=True)
    mobile_number = PhoneNumberField(_('mobile number'), blank=True, null=True)
    logo          = models.ImageField(upload_to=logo_media_upload, null=True, blank=True)
    status        = models.ForeignKey(CompanyStatus, related_name="company_status", on_delete=models.CASCADE)
    addresses     = GenericRelation(Address, related_query_name='company')
    owner         = models.ForeignKey(User,  related_name="company_owner", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} | {self.abn}"

    @property
    def address(self):
        return self.addresses.last()
