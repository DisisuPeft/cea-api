# Generated by Django 5.1.3 on 2025-06-01 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_escolar', '0006_alter_asignaciones_profesor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilegreso',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perfilingreso',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requisitoegreso',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requisitoingreso',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requisitopermanencia',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resultadoactualizacion',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resultadoaplicacion',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resultadocrecimiento',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
