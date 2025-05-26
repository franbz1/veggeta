from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('recepcion', 'Personal de Recepción'),
        ('administrador', 'Administrador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='cliente')
    telefono = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos.")],
        blank=True,
        null=True
    )
    documento_identidad = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.get_tipo_usuario_display()}"
    
    def es_cliente(self):
        return self.tipo_usuario == 'cliente'
    
    def es_personal_recepcion(self):
        return self.tipo_usuario == 'recepcion'
    
    def es_administrador(self):
        return self.tipo_usuario == 'administrador'

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Signal para crear automáticamente un perfil cuando se crea un usuario"""
    if created:
        # Determinar el tipo de usuario basado en si es superuser o staff
        if instance.is_superuser:
            tipo_usuario = 'administrador'
        elif instance.is_staff:
            tipo_usuario = 'recepcion'
        else:
            tipo_usuario = 'cliente'
            
        PerfilUsuario.objects.create(
            usuario=instance,
            tipo_usuario=tipo_usuario
        )

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Signal para guardar el perfil cuando se guarda el usuario"""
    try:
        instance.perfilusuario.save()
    except PerfilUsuario.DoesNotExist:
        # Si no existe el perfil, lo creamos
        if instance.is_superuser:
            tipo_usuario = 'administrador'
        elif instance.is_staff:
            tipo_usuario = 'recepcion'
        else:
            tipo_usuario = 'cliente'
            
        PerfilUsuario.objects.create(
            usuario=instance,
            tipo_usuario=tipo_usuario
        )
