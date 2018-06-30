# Generated by Django 2.0.6 on 2018-06-15 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180408_1525'),
        ('profiles', '0002_auto_20180512_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutor', to='core.Address', verbose_name='adresse'),
        ),
    ]