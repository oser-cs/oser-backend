"""Initialize admin users."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Management command to initialize admin users.

    Admin users are created according to the ADMINS setting.

    NOTE: For security reasons, admin users will not be initialized
    if any user already exists.
    """

    help = 'Initialize admin users.'

    def handle(self, *args, **kwargs):
        """Initialize admin users.

        Returns
        -------
        initialized : bool
            True if admin users were initialized, False otherwise.
        """
        if User.objects.exclude(email='AnonymousUser').count() == 0:
            password = settings.ADMIN_INITIAL_PASSWORD
            for name, email in settings.ADMINS:
                admin = User.objects.create_superuser(
                    email=email,
                    first_name=name,
                    password=password
                )
                admin.is_active = True
                admin.is_staff = True
                admin.is_admin = True
                admin.save()
                self.stdout.write(self.style.SUCCESS(
                    'Created {} (email: {})'
                    .format(name, email)
                ))
        else:
            self.stdout.write(self.style.ERROR(
                'Admin users can only be initialized if no users exist.'
            ))
