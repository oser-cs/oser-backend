from django.apps import AppConfig


class ShowcaseSiteConfig(AppConfig):
    name = 'showcase_site'
    verbose_name = 'Site vitrine'

    def ready(self):
        from . import signals  # noqa
