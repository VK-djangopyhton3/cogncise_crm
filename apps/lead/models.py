from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, User, BasicInformation
from common.app_utils import profile_unique_upload

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
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, related_name="lead_status", null=True, blank=True)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.CASCADE, related_name="lead_source", null=True, blank=True)
    lead_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lead_owner", null=True, blank=True)

    
class LeadAddress(models.Model):
    # Lead Address
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="lead_address", null=True, blank=True)