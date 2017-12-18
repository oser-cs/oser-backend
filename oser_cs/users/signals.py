"""App signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


# Create your signals here.

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    """Automatically creates a new profile for a newly created user."""
    if created and instance.profile_type:
        model = Profile.get_model(instance.profile_type)
        model.objects.create(user=instance)
