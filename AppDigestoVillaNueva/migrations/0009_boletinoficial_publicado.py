# Generated by Django 4.2.7 on 2023-12-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppDigestoVillaNueva', '0008_boletinoficial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boletinoficial',
            name='publicado',
            field=models.BooleanField(default=False),
        ),
    ]
