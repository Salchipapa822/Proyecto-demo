# Generated by Django 5.1.5 on 2025-02-27 16:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0010_rename_username_administrador_usuario_usuario_cedula_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='cedula',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cedula'),
        ),
    ]
