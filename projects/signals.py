"""Projects app signals."""

import logging
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Participation


logger = logging.getLogger('web.projects.signals')


@receiver(pre_delete, sender=Participation)
def delete_associated_form_entry(sender, instance: Participation,
                                 *args, **kwargs):
    """Delete the form entry associated to a participation being deleted."""
    entry = instance.entry
    if entry:
        entry.delete()
        logger.info('entry %s deleted', entry.id)
