# Generated by Django 2.2 on 2020-09-25 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_student_classtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='year',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='année'),
        ),
    ]