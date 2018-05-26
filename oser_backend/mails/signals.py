"""Mails app signals."""

from django.dispatch import Signal, receiver

from logs import get_logger

delivered = Signal(providing_args=['mail_from', 'subject', 'recipient_list'])
app_disabled = Signal(providing_args=['subject', 'recipient_list'])
notification_sent = Signal(providing_args=['instance', 'result'])

logger = get_logger('notifications')


@receiver(delivered)
def log_delivered(sender, mail_from, subject, recipient_list, **kwargs):
    logger.info('Sent email "%s" from %s to %s', subject, mail_from,
                recipient_list)


@receiver(app_disabled)
def log_app_disabled(sender, subject, recipient_list, **kwargs):
    logger.warning(
        'Email "%s" not sent to %s because MAILS_ENABLED is set to False',
        subject, recipient_list)
