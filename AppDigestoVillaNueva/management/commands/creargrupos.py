from django import apps as global_apps
from django.db.models import Q
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crea grupos y asigna permisos'

    def handle(self, *args, **options):
        self.stdout.write('Creando grupos y asignando permisos...')
        self.create_groups()

    def create_groups(self):
        Group = global_apps.apps.get_model('auth', 'Group')
        Permission = global_apps.apps.get_model('auth', 'Permission')

        # Define tus grupos y permisos aquí
        groups_permissions = {
            'OfProtocolo_Admin': ['add_decreto', 'change_decreto', 'view_decreto', 'delete_decreto', 'admin_decreto'],
            'OfProtocolo_Carga': ['add_decreto', 'change_decreto', 'view_decreto'],
            'OfProtocolo_SoloLectura': ['view_decreto']
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Grupo {group_name} creado.')

            for codename in permissions:
                perm = Permission.objects.get(codename=codename)
                group.permissions.add(perm)

            self.stdout.write(f'Permisos asignados al grupo {group_name}.')