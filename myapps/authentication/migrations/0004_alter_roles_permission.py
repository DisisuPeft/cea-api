# Generated by Django 5.1.3 on 2025-04-06 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_rename_role_roles_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='permission',
            field=models.ManyToManyField(related_name='permission', to='authentication.permissions'),
        ),
    ]
