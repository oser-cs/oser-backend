from django.apps import AppConfig


class MailsConfig(AppConfig):
    name = 'mails'

    def ready(self):
        from . import signals  # noqa
