# Generated by Django 2.2.3 on 2020-12-11 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0010_pokemon_next_evolution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='next_evolution',
            new_name='previous_evolution',
        ),
    ]