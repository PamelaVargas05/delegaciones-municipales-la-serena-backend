from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Crea los grupos y permisos operativos del sistema.'

    def handle(self, *args, **options):
        modelos = ['delegacion', 'meta', 'vecino', 'tiposolicitud', 'solicitudvecinal', 'atencionsolicitud']
        permisos = Permission.objects.filter(
            content_type__app_label__in=['delegaciones', 'solicitudes'],
            content_type__model__in=modelos,
        )
        permisos_usuario = Permission.objects.filter(
            content_type__app_label='auth',
            content_type__model='user',
            codename__in=['view_user', 'add_user', 'change_user', 'delete_user'],
        )
        grupos = {
            'Administrador': permisos | permisos_usuario,
            'Supervisor': permisos.filter(codename__startswith='view_') | permisos.filter(codename__startswith='change_'),
            'Administrativo': permisos.filter(codename__startswith='view_') | permisos.filter(codename__startswith='add_'),
        }
        for nombre, asignaciones in grupos.items():
            grupo, _ = Group.objects.get_or_create(name=nombre)
            grupo.permissions.set(asignaciones.distinct())
        self.stdout.write(self.style.SUCCESS('Roles configurados correctamente.'))
