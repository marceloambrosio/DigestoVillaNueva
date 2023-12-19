from django import apps as global_apps
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea permisos personalizados'

    def handle(self, *args, **options):
        self.stdout.write('Creando permisos personalizados...')
        self.create_custom_permission()

    def create_custom_permission(self):
        # Obtén el ContentType para el modelo Decreto
        Decreto = global_apps.apps.get_model('AppDigestoVillaNueva', 'Decreto')
        content_type = ContentType.objects.get_for_model(Decreto)

        # Crea el permiso personalizado
        permission = Permission.objects.create(
            codename='admin_decreto',
            name='Admin decreto',
            content_type=content_type,
        )
        self.stdout.write('Permiso personalizado creado.')