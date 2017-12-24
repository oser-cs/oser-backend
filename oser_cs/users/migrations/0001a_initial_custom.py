"""Custom initial migrations.

DO NOT REMOVE THIS MIGRATION.
"""

from django.db import migrations
from users.permissions import Groups

from django.contrib.auth.models import Group
from utils import group_exists


def create_initial_data(apps, schema_editor):
    """Create initial data here."""
    # Create the VP_TUTORAT
    if not group_exists(Groups.VP_TUTORAT):
        Group.objects.create(name=Groups.VP_TUTORAT)


def remove_initial_data(apps, schema_editor):
    """Remove the created initial data here."""
    Group.objects.filter(name=Groups.VP_TUTORAT).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_initial_data, remove_initial_data),
    ]
