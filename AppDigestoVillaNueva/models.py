from django.db import models
from datetime import date
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.utils import timezone
import os


# Create your models here.

class Documento(models.Model):
    fecha_creacion = models.DateField(default=timezone.now)
    descripcion = models.TextField(max_length=2000)
    publicado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='documentos_creados')
    ultima_modificacion = models.DateTimeField(auto_now=True)
    modificado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='documentos_modificados')

def upload_to_decreto(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'Decretos/Decreto-{0}-{1:04d}{2}'.format(instance.anio, instance.numero_decreto, extension)

class Decreto(Documento):
    numero_decreto = models.PositiveIntegerField(default=1)
    anio = models.IntegerField(default=date.today().year)
    fecha_publicacion = models.DateField(blank=True, null=True)
    archivo_pdf = models.FileField(upload_to=upload_to_decreto, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")], blank=True, null=True)

    def __str__(self):
        return "Decreto- " + str(self.anio) + "/" + str(self.numero_decreto)
    
def upload_to_ordenanza(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'Ordenanzas/Ordenanza-{0}-{1:04d}{2}'.format(instance.anio, instance.numero_ordenanza, extension)

class Ordenanza(Documento):
    numero_ordenanza = models.PositiveIntegerField(default=1)
    anio = models.IntegerField(default=date.today().year)
    fecha_publicacion = models.DateField(blank=True, null=True)
    archivo_pdf = models.FileField(upload_to=upload_to_ordenanza, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")], blank=True, null=True)

    def __str__(self):
        return "Ordenanza- " + str(self.anio) + "/" + str(self.numero_ordenanza)

def upload_to_resolucion(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'Resoluciones/Resolucion-{0}-{1:04d}{2}'.format(instance.anio, instance.numero_resolucion, extension)

class Resolucion(Documento):
    numero_resolucion = models.PositiveIntegerField(default=1)
    anio = models.IntegerField(default=date.today().year)
    fecha_publicacion = models.DateField(blank=True, null=True)
    archivo_pdf = models.FileField(upload_to=upload_to_resolucion, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")], blank=True, null=True)

    def __str__(self):
        return "Resolucion- " + str(self.anio) + "/" + str(self.numero_resolucion)

def upload_to_declaracion(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'Declaraciones/Declaracion-{0}-{1:04d}{2}'.format(instance.anio, instance.numero_declaracion, extension)

class Declaracion(Documento):
    numero_declaracion = models.PositiveIntegerField(default=1)
    anio = models.IntegerField(default=date.today().year)
    fecha_publicacion = models.DateField(blank=True, null=True)
    archivo_pdf = models.FileField(upload_to=upload_to_declaracion, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")], blank=True, null=True)

    def __str__(self):
        return "Declaracion- " + str(self.anio) + "/" + str(self.numero_declaracion)

def upload_to_boletin(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'BoletinOficial/Boletin-{0}{1}'.format(instance.fecha_creacion, extension)

class BoletinOficial(models.Model):
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    decretos = models.BooleanField(default=False)
    resoluciones = models.BooleanField(default=False)
    ordenanzas = models.BooleanField(default=False)
    declaraciones = models.BooleanField(default=False)
    archivo_pdf = models.FileField(upload_to=upload_to_boletin, blank=True, null=True)