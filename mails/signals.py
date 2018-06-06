"""Mails app signals."""

import logging
from django.conf import settings
from django.dispatch import Signal, receiver
from python_http_client import HTTPError


delivered = Signal(providing_args=['mail_from', 'subject', 'recipient_list'])
app_disabled = Signal(providing_args=['subject', 'recipient_list'])
failed = Signal(providing_args=['exception'])
notification_sent = Signal(providing_args=['instance', 'result'])

logger = logging.getLogger('web.notifications')


@receiver(delivered)
def log_delivered(sender, mail_from, subject, recipient_list, **kwargs):
    logger.info('Sent email "%s" from %s to %s', subject, mail_from,
                recipient_list)


@receiver(app_disabled)
def log_app_disabled(sender, subject, recipient_list, **kwargs):
    logger.warning(
        'Email "%s" not sent to %s because MAILS_ENABLED is set to False',
        subject, recipient_list)


@receiver(failed)
def log_failed(sender, exception, **kwargs):
    """Log an exception that occurred during a mail delivery."""
    if isinstance(exception, HTTPError):
        logger.exception(exception.body)
    else:
        logger.exception(exception)
    if settings.MAILS_RAISE_EXCEPTIONS:
        raise exception
