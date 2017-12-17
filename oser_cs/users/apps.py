from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Utilisateurs'

    def ready(self):
        from . import signals  # noqa
