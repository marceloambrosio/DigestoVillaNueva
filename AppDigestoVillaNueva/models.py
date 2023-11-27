from django.db import models
from datetime import date
from django.core.validators import FileExtensionValidator


# Create your models here.

class Documento(models.Model):
    fecha_creacion = models.DateField(default=date.today)
    descripcion = models.TextField(max_length=2000)
    publicado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

def upload_to_decreto(instance, filename):
    return 'Decretos/Decreto-{0}-{1:04d}.pdf'.format(instance.anio, instance.numero_decreto)

class Decreto(Documento):
    numero_decreto = models.PositiveIntegerField(default=1)
    anio = models.IntegerField(default=date.today().year)
    fecha_publicacion = models.DateField(blank=True, null=True)
    archivo_pdf = models.FileField(upload_to=upload_to_decreto, validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)

    def __str__(self):
        return "Decreto- " + str(self.anio) + "/" + str(self.numero_decreto)
