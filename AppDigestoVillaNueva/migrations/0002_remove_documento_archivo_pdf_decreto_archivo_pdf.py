# Generated by Django 4.2.7 on 2023-11-27 19:50

import AppDigestoVillaNueva.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppDigestoVillaNueva', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='archivo_pdf',
        ),
        migrations.AddField(
            model_name='decreto',
            name='archivo_pdf',
            field=models.FileField(blank=True, null=True, upload_to=AppDigestoVillaNueva.models.upload_to_decreto, validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
