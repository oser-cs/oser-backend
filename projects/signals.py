"""Projects app signals."""

import logging

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver, Signal

from . import notifications
from .models import Participation

logger = logging.getLogger('web.projects.signals')


pending = Signal(providing_args=('instance',))
valid = Signal(providing_args=('instance',))
accepted = Signal(providing_args=('instance',))
rejected = Signal(providing_args=('instance',))
cancelled = Signal(providing_args=('instance',))
deleted = Signal(providing_args=('instance',))
deleted_organizers = Signal(providing_args=('instance',))


def _send(cls, instance: Participation):
    cls(user=instance.user, edition=instance.edition).send()


@receiver(pre_delete, sender=Participation)
def delete_associated_form_entry(sender, instance: Participation, **kwargs):
    """Delete the form entry associated to a participation being deleted."""
    entry = instance.entry
    if entry:
        entry.delete()
        logger.info('entry %s deleted', entry.id)


@receiver(post_save, sender=Participation)
def send_state_notifications(sender, instance: Participation,
                             created, **kwargs):
    """Send notifications when the state of a participation has changed."""
    if not created and not instance.state_changed:
        return
    signals = {
        Participation.STATE_PENDING: pending,
        Participation.STATE_VALIDATED: valid,
        Participation.STATE_ACCEPTED: accepted,
        Participation.STATE_REJECTED: rejected,
        Participation.STATE_CANCELLED: cancelled,
    }
    if instance.state in signals.keys():
        signals[instance.state].send(Participation, instance=instance)


@receiver(pre_delete, sender=Participation)
def send_participation_deleted_notifications(sender, instance: Participation,
                                             **kwargs):
    """Send notifications when a participation is deleted."""
    deleted.send(Participation, instance=instance)


# Notiication senders

@receiver(pending)
def notify_pending(sender, instance, **kwargs):
    print('hello')
    _send(notifications.UserReceived, instance)
    _send(notifications.OrganizersReceived, instance)


@receiver(valid)
def notify_valid(sender, instance, **kwargs):
    _send(notifications.UserValid, instance)


@receiver(accepted)
def notify_accepted(sender, instance, **kwargs):
    _send(notifications.UserAccepted, instance)


@receiver(rejected)
def notify_rejected(sender, instance, **kwargs):
    _send(notifications.UserRejected, instance)


@receiver(cancelled)
def notify_cancelled(sender, instance, **kwargs):
    _send(notifications.UserCancelled, instance)
    _send(notifications.OrganizersCancelled, instance)


@receiver(deleted)
def notify_deleted(sender, instance, **kwargs):
    _send(notifications.UserDeleted, instance)
    _send(notifications.OrganizersDeleted, instance)
