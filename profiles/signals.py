"""Profile signals."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tutor


@receiver(post_save, sender=Tutor)
def add_created_tutor_to_staff(sender, instance, created, **kwargs):
    """When creating a tutor profile, automatically assign it as staff.

    This way they will be able to connect in the administration site.
    Note that they will not have any permission so their view of the admin
    site will be empty.
    """
    if created:
        instance.user.is_staff = True
        instance.user.save()
