# Generated by Django 2.0.3 on 2018-03-25 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase_site', '0003_auto_20180319_2254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-pinned', '-published'), 'verbose_name': 'article'},
        ),
    ]