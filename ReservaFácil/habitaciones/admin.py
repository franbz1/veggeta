from django.contrib import admin
from .models import Habitacion

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'capacidad', 'precio_por_noche', 'estado', 'fecha_creacion')
    list_filter = ('tipo', 'estado', 'capacidad', 'fecha_creacion')
    search_fields = ('numero', 'tipo', 'servicios_incluidos', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ['numero']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero', 'tipo', 'capacidad', 'precio_por_noche', 'estado')
        }),
        ('Detalles', {
            'fields': ('servicios_incluidos', 'descripcion'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
