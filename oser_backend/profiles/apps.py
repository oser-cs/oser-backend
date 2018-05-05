from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    verbose_name = 'Profils'

    def ready(self):
        from . import signals  # noqa
