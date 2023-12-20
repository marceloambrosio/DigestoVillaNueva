from django import apps as global_apps
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea permisos personalizados'

    def handle(self, *args, **options):
        self.stdout.write('Creando permisos personalizados...')
        self.create_custom_permission('Decreto', 'admin_decreto', 'Admin decreto')
        self.create_custom_permission('Resolucion', 'admin_resolucion', 'Admin resolucion')
        self.create_custom_permission('Ordenanza', 'admin_ordenanza', 'Admin ordenanza')
        self.create_custom_permission('Declaracion', 'admin_declaracion', 'Admin declaracion')
        self.create_custom_permission('BoletinOficial', 'admin_boletinoficial', 'Admin boletin oficial')

    def create_custom_permission(self, model_name, codename, name):
        # Obtén el ContentType para el modelo dado
        Model = global_apps.apps.get_model('AppDigestoVillaNueva', model_name)
        content_type = ContentType.objects.get_for_model(Model)

        # Verifica si el permiso ya existe
        try:
            permission = Permission.objects.get(content_type=content_type, codename=codename)
            self.stdout.write(f'El permiso {name} ya existe.')
        except Permission.DoesNotExist:
            # Si el permiso no existe, créalo
            permission = Permission.objects.create(
                codename=codename,
                name=name,
                content_type=content_type,
            )
            self.stdout.write(f'Permiso personalizado {name} creado.')