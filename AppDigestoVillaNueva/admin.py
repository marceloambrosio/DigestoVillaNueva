from django.contrib import admin
from .models import Documento, Decreto

# Register your models here.

class DocumentoAdmin(admin.ModelAdmin):
    search_fields = ('fecha_creacion'),
    ordering = ['fecha_creacion']

class DecretoAdmin(admin.ModelAdmin):
    search_fields = ('anio','numero_decreto'),
    ordering = ['anio','numero_decreto','fecha_publicacion']

admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Decreto, DecretoAdmin)