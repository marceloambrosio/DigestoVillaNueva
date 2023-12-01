# Generated by Django 4.2.7 on 2023-12-01 11:58

import AppDigestoVillaNueva.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppDigestoVillaNueva', '0002_remove_documento_archivo_pdf_decreto_archivo_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='creado_por',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='documentos_creados', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='modificado_por',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='documentos_modificados', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='ultima_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='decreto',
            name='archivo_pdf',
            field=models.FileField(blank=True, null=True, upload_to=AppDigestoVillaNueva.models.upload_to_decreto, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='ERROR, el archivo tiene que estar en formato PDF.')]),
        ),
    ]
