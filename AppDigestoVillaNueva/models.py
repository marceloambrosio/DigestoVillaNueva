from django.db import models
from datetime import date

# Create your models here.

class Documento(models.Model):
    fecha_creacion = models.DateField(default=date.today)
    descripcion = models.TextField(max_length=2000)
    archivo_pdf = models.FileField(blank=True, null=True)
    publicado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

class Decreto(Documento):
    numero_decreto = models.PositiveIntegerField(default=1)
    anio = models.IntegerField(default=date.today().year)
    fecha_publicacion = models.DateField(blank=True, null=True)