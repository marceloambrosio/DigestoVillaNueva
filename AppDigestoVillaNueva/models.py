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
