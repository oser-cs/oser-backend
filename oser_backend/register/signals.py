"""Register signals."""

from django.contrib.auth import get_user_model
from django.dispatch import Signal, receiver

from profiles.models import Student

from .models import Registration

User = get_user_model()


registration_created = Signal(providing_args=('instance', 'password'))


@receiver(registration_created, sender=Registration)
def create_user_and_student(sender, instance: Registration,
                            password: str, **kwargs):
    """Create a user and student after on a registration_created signal."""
    user = User.objects.create_user(
        email=instance.email,
        password=password,
        first_name=instance.first_name,
        last_name=instance.last_name,
        date_of_birth=instance.date_of_birth,
        phone_number=instance.phone,
    )

    Student.objects.create(
        user=user,
        school=instance.school,
        registration=instance,
    )
