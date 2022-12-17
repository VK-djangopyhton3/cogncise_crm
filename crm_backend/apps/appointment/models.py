from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstract_models import BaseModel
from job.models import Job
from company.models import Company

class WorkType(BaseModel):
    title = models.CharField( _("title"), max_length=100)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title}"


class Appointment(BaseModel):
    work_type  = models.ForeignKey(WorkType, related_name="work_type",   on_delete=models.CASCADE)
    job  = models.ForeignKey(Job, related_name="job_apointment",   on_delete=models.CASCADE)
    instruction = models.CharField( _("instruction"), max_length=100)
    company = models.ForeignKey(Company, related_name="appointment_company", on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job.title}"


class SechduleAppointment(BaseModel):
    appointment  = models.ForeignKey(Appointment, related_name="appointment",   on_delete=models.CASCADE)
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    duration = models.BigIntegerField(_("Duration"), null=True, blank=True)
    lead_route_distance = models.BooleanField( _("Lead Route Distance"), default=False)
    ineligible_suburbs = models.BooleanField( _("Ineligible Suburbs"), default=False)
    all_agents = models.BooleanField( _("All Agents"), default=False)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.appointment.job.title}"


class TimeSlots(BaseModel):
    sechdule_appointment  = models.ForeignKey(SechduleAppointment, related_name="sechdule_appointment",   on_delete=models.CASCADE)
    in_time = models.BigIntegerField(_("in time"), null=True, blank=True)
    out_time = models.BigIntegerField(_("out time"), null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sechdule_appointment.appointment.job.title}"
