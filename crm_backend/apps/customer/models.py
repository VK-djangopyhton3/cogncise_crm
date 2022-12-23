from django.db.models import Q
from common.common_model_imports import *
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from core.models import CustomeUserManager, Group
from shared.models import Address

User = get_user_model()

class CustomerManager(CustomeUserManager):
    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(role_type = 'customer', is_customer = True)


class Customer(User):
    objects = CustomerManager()
    addresses = GenericRelation(Address, related_query_name='customer_address', null = True, blank = True)

    class Meta:
        proxy = True
        ordering = ['-created_at']

    def __init__(self, *args, **kwargs):
        self._meta.get_field('role_type').default = 'customer'
        self._meta.get_field('is_customer').default = True
        super(Customer, self).__init__(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} | {self.last_name}" # type: ignore

    @property
    def address(self):
        return self.addresses.last()
    
    @classmethod
    def create_record(cls, **kwargs):
        customer = cls.objects.filter((Q(mobile_number=kwargs.get('mobile_number', None)) | Q(email__iexact=kwargs.get('email')))).first()
        if customer is not None:
            return customer

        kwargs.update({'role_type': 'customer', 'is_customer': True })
        if 'username' not in kwargs:
            kwargs.update({ 'username': kwargs['email'] })
        customer = cls.objects.create(**kwargs)
        role = Group.customer()
        customer.groups.add(role)
        customer.save()
            
        return customer
