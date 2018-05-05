"""App signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tutor


# Create your signals here.

@receiver(post_save, sender=Tutor)
def add_created_tutor_to_staff(sender, instance, created, **kwargs):
    """When creating a tutor profile, automatically assign it as staff."""
    if created:
        instance.user.is_staff = True
        instance.user.save()
