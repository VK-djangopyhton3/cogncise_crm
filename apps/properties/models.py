from django.db import models


# Create your models here.

class PropertyTypes(models.Model):
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.unit_type


class Property(models.Model):
    building_name = models.CharField(max_length=255)
    level_no = models.IntegerField(null=True, blank=True)
    unit_no = models.IntegerField(null=True, blank=True)
    lot_no = models.IntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=255)
    street_type = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

