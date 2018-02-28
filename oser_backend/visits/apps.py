from django.apps import AppConfig


class VisitsConfig(AppConfig):
    name = 'visits'
    verbose_name = 'Sorties'

    def ready(self):
        from . import signals
