# Generated by Django 2.2 on 2020-09-13 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20180911_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='addressNumber',
            field=models.IntegerField(blank=True, null=True, verbose_name='numéro de rue'),
        ),
        migrations.AddField(
            model_name='student',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='nom de ville'),
        ),
        migrations.AddField(
            model_name='student',
            name='dependantsNumber',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name="numero d'urgence"),
        ),
        migrations.AddField(
            model_name='student',
            name='fatherActivity',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='metier du pere'),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='genre'),
        ),
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='nom du niveau de la classe'),
        ),
        migrations.AddField(
            model_name='student',
            name='motherActivity',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='metier de la mere'),
        ),
        migrations.AddField(
            model_name='student',
            name='parentsEmail',
            field=models.EmailField(blank=True, max_length=20, null=True, verbose_name='adresse mail parentale'),
        ),
        migrations.AddField(
            model_name='student',
            name='parentsPhone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='numéro de téléphone parental'),
        ),
        migrations.AddField(
            model_name='student',
            name='parentsStatus',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='statut des parents'),
        ),
        migrations.AddField(
            model_name='student',
            name='personnalPhone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='numéro de téléphone personnel'),
        ),
        migrations.AddField(
            model_name='student',
            name='scholarship',
            field=models.BooleanField(blank=True, null=True, verbose_name='boursier'),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name="nom de l'ecole"),
        ),
        migrations.AddField(
            model_name='student',
            name='street',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='nom de rue'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='promotion',
            field=models.IntegerField(choices=[(2023, '2023'), (2022, '2022'), (2021, '2021'), (2020, '2020'), (2019, '2019')], default=2023),
        ),
    ]
