# Generated by Django 5.0.4 on 2024-04-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_campeonato_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campeonato',
            name='descripcion',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
