# Generated by Django 5.0.4 on 2024-04-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_equipos_campeonato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipos',
            name='estado',
        ),
        migrations.AddField(
            model_name='equiposcampeonato',
            name='estado',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
