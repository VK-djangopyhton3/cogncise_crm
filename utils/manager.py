from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email,name, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        user = self.model(
            email=email,
            name=name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password, **extra_fields):
        return self._create_user(email, name, password, False, False, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        user = self._create_user(email, name, password, True, True, **extra_fields)
        return user
