from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from utils.manager import UserManager


# Create your models here.
class CrmUser(AbstractBaseUser, PermissionsMixin):
    # User info
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=254, unique=True, null=True, blank=True)
    name = models.CharField(max_length=254, null=True)
    # profile_pic     =   models.ImageField(upload_to='media/profile_pic',blank=True,null=True)

    # Account info
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/accounts/%i/" % (self.pk)
