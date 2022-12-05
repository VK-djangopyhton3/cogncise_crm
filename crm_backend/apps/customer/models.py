from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from core.abstract_models import BaseModel, BasicInformation
from shared.models import Address

User = get_user_model()

class Customer(BaseModel):
    addresses = GenericRelation(Address, related_query_name='customer_address', null = True, blank = True)
    user     = models.ForeignKey(User,  related_name="customer_owner", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.first_name} | {self.user.last_name}"

    @property
    def address(self):
        return self.addresses.last()
