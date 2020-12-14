# Generated by Django 2.2.3 on 2020-12-14 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0019_auto_20201212_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='next_evolution', related_query_name='next_evolution', to='pokemon_entities.Pokemon', verbose_name='Родитель'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pokemon_entities.Pokemon', verbose_name='gокемон'),
        ),
    ]
