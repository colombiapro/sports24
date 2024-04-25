# Generated by Django 5.0.4 on 2024-04-24 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_equipos_fecha_creacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desafios',
            name='equipo1',
        ),
        migrations.RemoveField(
            model_name='desafios',
            name='equipo2',
        ),
        migrations.AlterField(
            model_name='desafios',
            name='ganador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.equipos'),
        ),
        migrations.CreateModel(
            name='HistorialEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipos')),
            ],
        ),
    ]