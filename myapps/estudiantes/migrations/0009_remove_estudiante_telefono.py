# Generated by Django 5.1.3 on 2025-05-16 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0008_remove_estudiante_nivel_educativo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='telefono',
        ),
    ]
