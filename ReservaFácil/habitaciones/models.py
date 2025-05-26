from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Habitacion(models.Model):
    TIPOS_HABITACION = [
        ('individual', 'Individual'),
        ('doble', 'Doble'),
        ('matrimonial', 'Matrimonial'),
        ('suite', 'Suite'),
        ('familiar', 'Familiar'),
        ('presidencial', 'Presidencial'),
    ]
    
    ESTADOS_HABITACION = [
        ('disponible', 'Disponible'),
        ('mantenimiento', 'Mantenimiento'),
        ('reservada', 'Reservada'),
        ('ocupada', 'Ocupada'),
    ]
    
    numero = models.CharField(
        max_length=10, 
        unique=True,
        verbose_name="Número de Habitación",
        help_text="Número único de la habitación (ej: 101, 201A)"
    )
    tipo = models.CharField(
        max_length=20, 
        choices=TIPOS_HABITACION,
        verbose_name="Tipo de Habitación"
    )
    precio_por_noche = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio por Noche",
        help_text="Precio en pesos colombianos"
    )
    capacidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Capacidad",
        help_text="Número máximo de huéspedes"
    )
    servicios_incluidos = models.TextField(
        blank=True,
        verbose_name="Servicios Incluidos",
        help_text="Descripción de servicios incluidos (WiFi, TV, minibar, etc.)"
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_HABITACION,
        default='disponible',
        verbose_name="Estado"
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción adicional de la habitación"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
        ordering = ['numero']
    
    def __str__(self):
        return f"Habitación {self.numero} - {self.get_tipo_display()}"
    
    def esta_disponible(self):
        """Verifica si la habitación está disponible"""
        return self.estado == 'disponible'
    
    def precio_formateado(self):
        """Retorna el precio formateado en pesos colombianos"""
        return f"${self.precio_por_noche:,.0f} COP"
