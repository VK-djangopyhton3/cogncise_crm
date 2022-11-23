from django.db import models
from django.db.models import UniqueConstraint, Q

from apps.customer.models import CustomerInfo


# Create your models here.

class PropertyTypes(models.Model):
    type_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name


class StreetTypes(models.Model):
    type_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name


class Property(models.Model):
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyTypes, on_delete=models.CASCADE)
    building_name = models.CharField(max_length=255)
    level_no = models.IntegerField(null=True, blank=True)
    unit_no = models.IntegerField(null=True, blank=True)
    lot_no = models.IntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=255)
    street_type = models.ForeignKey(StreetTypes, null=True, blank=True, on_delete=models.CASCADE)
    suffix = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lga = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_business = models.BooleanField(default=False)
    is_billing_address = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.customer.name

    class Meta:
        constraints = [
            UniqueConstraint(fields=['customer'], condition=Q(is_billing_address=True), name='unique_billing_address'),
        ]
