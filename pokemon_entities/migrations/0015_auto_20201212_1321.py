# Generated by Django 2.2.3 on 2020-12-12 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_auto_20201212_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Имя'),
        ),
    ]
