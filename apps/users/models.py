from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.company.models import Companies
from utils.manager import UserManager
from utils.options import USER_ROLES


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    # User info
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=254, unique=True, null=True, blank=True)
    name = models.CharField(max_length=254)
    # profile_pic     =   models.ImageField(upload_to='media/profile_pic',blank=True,null=True) # uncomment needed

    # Account info
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name + '(' + self.email + ')'


class UserRoles(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=15, choices=USER_ROLES)
