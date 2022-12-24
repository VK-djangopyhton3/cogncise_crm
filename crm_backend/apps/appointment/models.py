from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstract_models import BaseModel
from job.models import Job
from company.models import Company

ASSESSMENT_BY = (
    ('field_worker','FIELD WORKER'),
    ('customer', 'CUSTOMER'),
)

class WorkType(BaseModel):
    title = models.CharField( _("title"), max_length=100)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title}"

class AppointmentStatus(BaseModel):
    title = models.CharField( _("title"), max_length=100)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title}"

class Appointment(BaseModel):
    assessment_by = models.CharField(max_length=15, choices=ASSESSMENT_BY, default='field_worker')
    work_type  = models.ForeignKey(WorkType, related_name="work_type",   on_delete=models.CASCADE)
    apointment_status  = models.ForeignKey(AppointmentStatus, related_name="apointment_status",   on_delete=models.CASCADE,  null=True, blank=True)
    job  = models.ForeignKey(Job, related_name="job_apointment",   on_delete=models.CASCADE)
    instruction = models.CharField( _("instruction"), max_length=100)
    company = models.ForeignKey(Company, related_name="appointment_company", on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    duration = models.BigIntegerField(_("Duration"), null=True, blank=True)
    load_route_distance = models.BooleanField( _("Lead Route Distance"), default=False)
    ineligible_suburbs = models.BooleanField( _("Ineligible Suburbs"), default=False)
    all_agents = models.BooleanField( _("All Agents"), default=False)
    waiting_list = models.BooleanField( _("Waiting List"), default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job.title}"
    
    @property
    def time_slots(self):
        return self.schedule_appointment.all() # type: ignore


class TimeSlots(BaseModel):
    schedule_appointment  = models.ForeignKey(Appointment, related_name="schedule_appointment",   on_delete=models.CASCADE, null=True, blank=True)
    in_time = models.BigIntegerField(_("in time"), null=True, blank=True)
    out_time = models.BigIntegerField(_("out time"), null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.schedule_appointment.appointment.job.title}" # type: ignore
