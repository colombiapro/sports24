# Generated by Django 5.0.4 on 2024-04-23 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_equiposcampeonato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipos',
            name='campeonato',
        ),
    ]
