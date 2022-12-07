from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    # uuid         = models.CharField(default=gen_uuid, max_length=8, editable=False, unique=True, db_index=True)
    created_at   = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at   = models.DateTimeField(auto_now=True, db_index=True)
    is_deleted   = models.BooleanField( _('is_deleted'), default=False, help_text=_('Designates whether this user should be treated as delete user. '),)
    objects      = SoftDeleteManager()
    with_deleted = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class BasicInformation(BaseModel):
    first_name    = models.CharField( _("first name"), max_length=30)
    last_name     = models.CharField( _("last name"), max_length=30, null=True, blank=True )
    email         = models.EmailField( _("Email address"))
    mobile_number = PhoneNumberField( _('mobile number'), blank=True, null=True )

    class Meta:
        abstract = True
