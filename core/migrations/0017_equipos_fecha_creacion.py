# Generated by Django 5.0.4 on 2024-04-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_eventos_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipos',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]