from django.db import migrations
from ..models import Participation


def postgres_migration_prep(apps, schema_editor):
    participations = Participation.objects.filter(accepted=True)
    for participation in participations:
        participation.accepted = 1


class Migration(migrations.Migration):

    dependencies = [("visits", "0002_visit_context_sheet")]

    operations = [
        migrations.RunPython(postgres_migration_prep,
                             migrations.RunPython.noop)
    ]
