# Generated by Django 5.1.3 on 2025-05-01 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_alter_campania_fecha_actualizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campania',
            name='fuente',
        ),
    ]
