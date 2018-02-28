"""Visits signals."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db import transaction
from guardian.shortcuts import assign_perm
from visits.models import Visit


@receiver(post_save, sender=Visit)
def sync_organizers_group(sender, instance, **kwargs):
    """Sync visit and its organizers group.

    Create the group if visit has none, updates the group name otherwise.
    """
    visit = instance
    if not visit.organizers_group:
        with transaction.atomic():
            group_name = visit.organizers_group_name
            group = Group.objects.create(name=group_name)
            group.save()
            visit.organizers_group = group
            assign_perm('manage_visit', group, visit)
    elif visit.organizers_group.name != visit.organizers_group_name:
        with transaction.atomic():
            # update group name
            group = visit.organizers_group
            old_name = group.name
            group.name = visit.organizers_group_name
            group.save()
            # delete old group
            Group.objects.filter(name=old_name).delete()
