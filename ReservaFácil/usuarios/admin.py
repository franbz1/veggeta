from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)

# Desregistrar el UserAdmin original y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_usuario', 'telefono', 'documento_identidad', 'fecha_creacion')
    list_filter = ('tipo_usuario', 'fecha_creacion')
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name', 'documento_identidad')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
