"""Base mails commands."""

from django.core.management import CommandError
from django.utils.module_loading import import_string


class MailsCommandMixin:
    """Define common functionnality for mails commands."""

    def add_arguments(self, parser):
        parser.add_argument(
            'notification_cls',
            help='Notification class to use.')

    def get_notification(self, kwargs):
        notification_cls = import_string(kwargs['notification_cls'])
        try:
            notification = notification_cls.example()
        except NotImplementedError:
            name = notification_cls.__name__
            raise CommandError(
                f'{name} cannot be rendered because '
                f'{name}.example() is not implemented.')
        return notification
