from django.contrib import admin
from .models import Documento, Decreto

# Register your models here.

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'fecha_creacion', 'creado_por', 'ultima_modificacion', 'modificado_por')
    search_fields = ('fecha_creacion'),
    ordering = ['fecha_creacion']

class DecretoAdmin(admin.ModelAdmin):
    list_display = ('numero_decreto', 'anio', 'fecha_publicacion', 'fecha_creacion', 'creado_por', 'ultima_modificacion', 'modificado_por')
    search_fields = ('anio','numero_decreto'),
    ordering = ['anio','numero_decreto','fecha_publicacion']

admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Decreto, DecretoAdmin)