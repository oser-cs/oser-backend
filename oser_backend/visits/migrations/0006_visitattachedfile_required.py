# Generated by Django 2.0.2 on 2018-03-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0005_remove_visitattachedfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitattachedfile',
            name='required',
            field=models.BooleanField(default=True, verbose_name='requis'),
        ),
    ]