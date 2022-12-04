"""Config for django signals"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from core.models import User
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

@receiver(post_save, sender=Group)
def post_register(sender, instance: Group, created, **kwargs):

    if created:
        try:

            if not instance.slug:
                instance.slug = slugify(instance.name)  # type: ignore
                instance.save()
        except Exception as e:
            pass

