"""Send a notification."""

from ..base import MailsCommandMixin
from django.core.management import BaseCommand


class Command(MailsCommandMixin, BaseCommand):
    """Send a notification."""

    help = 'Send a notification.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'recipient', help='Email of the notification recipient.')

    def handle(self, *args, **kwargs):
        recipient = kwargs['recipient']
        notification = self.get_notification(kwargs)
        notification.force_recipients([recipient])
        notification.send()
        if notification.sent:
            self.stdout.write(self.style.SUCCESS(
                f'Notification email sent to {recipient}.'))
        else:
            self.stderr.write(
                'Notification email not sent (see above for logs).')
