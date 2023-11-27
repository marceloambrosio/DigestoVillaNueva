# Generated by Django 4.2.7 on 2023-11-27 13:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(default=datetime.date.today)),
                ('descripcion', models.TextField(max_length=2000)),
                ('archivo_pdf', models.FileField(blank=True, null=True, upload_to='')),
                ('publicado', models.BooleanField(default=False)),
                ('eliminado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Decreto',
            fields=[
                ('documento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AppDigestoVillaNueva.documento')),
                ('numero_decreto', models.PositiveIntegerField(default=1)),
                ('anio', models.IntegerField(default=2023)),
                ('fecha_publicacion', models.DateField(blank=True, null=True)),
            ],
            bases=('AppDigestoVillaNueva.documento',),
        ),
    ]