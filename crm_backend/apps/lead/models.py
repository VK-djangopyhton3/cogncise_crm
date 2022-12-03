from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from core.abstract_models import BaseModel, BasicInformation
from company.models import Company
from shared.models import Address

User = get_user_model()

class LeadStatus(BaseModel):
    title = models.CharField(_("Lead status"), max_length=100)

    class Meta:
        verbose_name = _("Lead Status")
        verbose_name_plural = _("Lead Status")

    def __str__(self):
        return self.title


class LeadSource(BaseModel):
    title = models.CharField(_("Lead source"), max_length=100)

    class Meta:
        verbose_name = _("Lead Source")
        verbose_name_plural = _("Lead Sources")

    def __str__(self):
        return self.title


class Lead(BasicInformation):
    addresses = GenericRelation(Address,      related_query_name='lead')
    status    = models.ForeignKey(LeadStatus, related_name="lead_status",   on_delete=models.CASCADE)
    source    = models.ForeignKey(LeadSource, related_name="lead_source",   on_delete=models.CASCADE)
    owner     = models.ForeignKey(User,       related_name="lead_owner",    on_delete=models.CASCADE)
    customer  = models.ForeignKey(User,       related_name="lead_customer", on_delete=models.CASCADE, null=True, blank=True)
    company   = models.ForeignKey(Company,    related_name="lead_company",  on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.source}"

    @property
    def address(self):
        return self.addresses.last()
