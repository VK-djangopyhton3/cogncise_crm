from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from core.abstract_models import BaseModel, BasicInformation
from shared.models import Address

User = get_user_model()

class Company(BaseModel):
    name      = models.CharField( _("name"), max_length=30)
    abn       = models.CharField( _("ABN"),  max_length=30, unique=True)
    addresses = GenericRelation(Address, related_query_name='company')
    owner     = models.ForeignKey(User,  related_name="company_owner", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return f"{self.name} | {self.abn}"

    @property
    def address(self):
        return self.addresses.last()
