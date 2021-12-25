# Generated by Django 2.2 on 2021-12-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_visit_context_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='accepted',
            field=models.IntegerField(choices=[(0, 'refusé'), (1, 'accepté'), (2, 'en attente')], default=0, help_text='Cocher pour confirmer au tutoré sa participation à la sortie.'),
        ),
    ]
