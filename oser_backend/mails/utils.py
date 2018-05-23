"""Mail utilities."""

from django.core.mail import send_mail
from .settings import NOTIFICATIONS_ADDRESS
from django.conf import settings


def send_mail_notification(subject, message, recipient_list, **kwargs):
    """Send an email from the notifications address.

    If notifications are inactive, does nothing.
    """
    if settings.MAILS_ENABLED:
        send_mail(
            subject, message, NOTIFICATIONS_ADDRESS, recipient_list,
            **kwargs)
        print(f'MAILER: sent email "{subject}" to {recipient_list}')
    else:
        print('MAILER: skipped because emails are disabled')
