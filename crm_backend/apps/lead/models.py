from django.utils.translation import gettext_lazy as _
from common.common_model_imports import *
from common.app_utils import profile_unique_upload

from core.abstract_models import BaseModel, BasicInformation, Address

User = get_user_model()


class LeadStatus(BaseModel):
    title = models.CharField(_("Lead status"), max_length=100)

    def __str__(self):
        return self.title

class LeadSource(BaseModel):
    title = models.CharField(_("Lead source"), max_length=100)

    def __str__(self):
        return self.title

class Lead(BasicInformation):
    # Customer Detail
    lead_status = models.ForeignKey(LeadStatus, related_name="lead_status", null=True, blank=True, on_delete=models.CASCADE)
    lead_source = models.ForeignKey(LeadSource, related_name="lead_source", null=True, blank=True, on_delete=models.CASCADE)
    lead_owner = models.ForeignKey(User, related_name="lead_owner", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('lead')
        verbose_name_plural = _('leads')

    def __str__(self):
        return f"{self.first_name} {self.lead_source}"


class LeadAddress(Address):
    # Lead Address
    lead = models.ForeignKey(Lead, related_name="lead_address", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.building_number} {self.street_name} {self.state} {self.pincode}"

