"""Render a notification."""

from ..base import MailsCommandMixin
from django.core.management import BaseCommand


class Command(MailsCommandMixin, BaseCommand):
    """Render a notification."""

    help = 'Render a notification.'

    def handle(self, *args, **kwargs):
        notification = self.get_notification(kwargs)
        print(notification.render())
