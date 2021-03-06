# Generated by Django 2.0.7 on 2018-09-11 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutor', to=settings.AUTH_USER_MODEL, verbose_name='utilisateur'),
        ),
        migrations.AddField(
            model_name='student',
            name='registration',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='register.Registration', verbose_name="dossier d'inscription"),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL, verbose_name='utilisateur'),
        ),
    ]
