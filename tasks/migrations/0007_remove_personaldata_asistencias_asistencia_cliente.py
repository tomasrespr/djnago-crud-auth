# Generated by Django 5.2.1 on 2025-05-22 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_personaldata_asistencias_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaldata',
            name='asistencias',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='tasks.personaldata'),
            preserve_default=False,
        ),
    ]
