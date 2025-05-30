# Generated by Django 5.1.3 on 2025-04-23 04:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0006_alter_institucionacademica_empresa'),
        ('maestros', '0002_maestro_fecha_actualizacion_maestro_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maestro',
            name='especialidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maestro_especialidad', to='catalogos.especialidades'),
        ),
    ]
