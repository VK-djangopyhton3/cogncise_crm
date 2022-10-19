from django.db import models


# Create your models here.
class Companies(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    company_address = models.CharField(max_length=255)
    ABN = models.CharField(max_length=255,null=True, unique=True)

    def __str__(self):
        return self.company_name

