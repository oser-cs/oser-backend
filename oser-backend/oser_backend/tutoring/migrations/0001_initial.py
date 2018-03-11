# Generated by Django 2.0.2 on 2018-03-01 22:32

import datetime
import django.core.validators
from django.db import migrations, models
import tutoring.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('name', models.CharField(help_text='Nom du lycée', max_length=200, verbose_name='nom')),
                ('uai_code', models.CharField(help_text="Code UAI (ex-RNE) de l'établissement. Celui-ci est composé de 7 chiffres et une lettre. Ce code est répertorié dans l'annuaire des établissements sur le site du ministère de l'Éducation Nationale.", max_length=8, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message="Un code UAI doit être composé de 7 chiffres suivis d'une lettre.", regex='^\\d{7}[a-zA-Z]$')], verbose_name='code UAI')),
                ('address', models.CharField(help_text='Adresse complète du lycée', max_length=200, verbose_name='adresse')),
            ],
            options={
                'verbose_name': 'lycée',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TutoringGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='nom')),
            ],
            options={
                'verbose_name': 'groupe de tutorat',
                'verbose_name_plural': 'groupes de tutorat',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TutoringSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('start_time', models.TimeField(default=tutoring.models.default_start_time, verbose_name='heure de début')),
                ('end_time', models.TimeField(default=tutoring.models.default_end_time, verbose_name='heure de fin')),
            ],
            options={
                'verbose_name': 'séance de tutorat',
                'verbose_name_plural': 'séances de tutorat',
                'ordering': ('date', 'start_time'),
            },
        ),
        migrations.CreateModel(
            name='TutorTutoringGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_leader', models.BooleanField(default=False)),
            ],
        ),
    ]
