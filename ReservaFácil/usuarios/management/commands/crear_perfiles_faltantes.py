from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Crea perfiles de usuario para usuarios que no los tienen'

    def handle(self, *args, **options):
        usuarios_sin_perfil = User.objects.filter(perfilusuario__isnull=True)
        
        if not usuarios_sin_perfil.exists():
            self.stdout.write(
                self.style.SUCCESS('Todos los usuarios ya tienen perfiles asociados.')
            )
            return

        perfiles_creados = 0
        
        for usuario in usuarios_sin_perfil:
            # Determinar el tipo de usuario
            if usuario.is_superuser:
                tipo_usuario = 'administrador'
            elif usuario.is_staff:
                tipo_usuario = 'recepcion'
            else:
                tipo_usuario = 'cliente'
            
            # Crear el perfil
            PerfilUsuario.objects.create(
                usuario=usuario,
                tipo_usuario=tipo_usuario
            )
            
            perfiles_creados += 1
            self.stdout.write(
                f'Perfil creado para usuario: {usuario.username} (tipo: {tipo_usuario})'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Se crearon {perfiles_creados} perfiles de usuario exitosamente.'
            )
        ) 