# Generated by Django 2.0.3 on 2018-04-07 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registration',
            options={'ordering': ('-submitted',), 'verbose_name': 'inscription administrative', 'verbose_name_plural': 'inscriptions administratives'},
        ),
    ]
