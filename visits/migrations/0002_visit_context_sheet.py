# Generated by Django 2.2 on 2021-05-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='context_sheet',
            field=models.FileField(blank=True, help_text='Informe le lycéen de détails sur le contexte. Tout format supporté, PDF recommandé.', null=True, upload_to='visits/context_sheets/', verbose_name='fiche contexte'),
        ),
    ]
