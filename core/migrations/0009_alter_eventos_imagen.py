# Generated by Django 5.0.4 on 2024-04-23 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_eventos_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='imagen',
            field=models.ImageField(default='eventos_imagenes/udenar.png', upload_to='eventos_imagenes/'),
        ),
    ]
