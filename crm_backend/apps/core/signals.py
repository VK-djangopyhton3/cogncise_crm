"""Config for django signals"""
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User, Group, Role
from common import app_utils


@receiver(post_save, sender=get_user_model())
def post_register(sender, instance: get_user_model(), created, **kwargs):
    """Sends mail/message to users after registeration

    Parameters
    ----------
    sender: get_user_model()

    instance: get_user_model()

    created: bool
    """


    if created:
        try:
            pass
            # instance.is_active = True
            # instance.save()
        except Exception as e:
            pass


@receiver(post_save, sender=Role)
def post_register(sender, instance: Role, created, **kwargs):
    """Sends mail/message to users after registeration

    Parameters
    ----------
    sender: get_user_model()

    instance: get_user_model()

    created: bool
    """


    if created:
        try:
            pass
            # instance.is_active = True
            # instance.save()
        except Exception as e:
            pass

