"""Visits app signals."""

from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from .models import Participation
from .notifications import Accepted, Rejected

accepted_changed = Signal()


@receiver(post_save, sender=Participation)
def fire_accepted_changed(sender, instance: Participation, created, **kwargs):
    """Fire an event if the participation status has changed."""
    if created or instance.accepted_changed():
        accepted_changed.send(sender=sender, instance=instance)


@receiver(accepted_changed)
def notify_participation(sender, instance: Participation, **kwargs):
    """Send notification to user depending on their participation status.

    The notification is only sent if the participation status has changed.
    """
    if instance.accepted is None:
        return
    notification_cls = Accepted if instance.accepted else Rejected
    notification_cls(user=instance.user, visit=instance.visit).send()
