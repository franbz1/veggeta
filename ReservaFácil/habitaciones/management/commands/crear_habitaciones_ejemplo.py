from django.core.management.base import BaseCommand
from habitaciones.models import Habitacion
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea habitaciones de ejemplo para probar el sistema'

    def handle(self, *args, **options):
        habitaciones_ejemplo = [
            {
                'numero': '101',
                'tipo': 'individual',
                'precio_por_noche': Decimal('80000'),
                'capacidad': 1,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar',
                'estado': 'disponible',
                'descripcion': 'Habitación individual cómoda y moderna con vista a la ciudad.'
            },
            {
                'numero': '102',
                'tipo': 'doble',
                'precio_por_noche': Decimal('120000'),
                'capacidad': 2,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar, balcón',
                'estado': 'disponible',
                'descripcion': 'Habitación doble espaciosa con dos camas individuales y balcón.'
            },
            {
                'numero': '201',
                'tipo': 'matrimonial',
                'precio_por_noche': Decimal('150000'),
                'capacidad': 2,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar, jacuzzi',
                'estado': 'disponible',
                'descripcion': 'Habitación matrimonial romántica con cama king size y jacuzzi.'
            },
            {
                'numero': '202',
                'tipo': 'suite',
                'precio_por_noche': Decimal('250000'),
                'capacidad': 4,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar, sala de estar, balcón con vista panorámica',
                'estado': 'disponible',
                'descripcion': 'Suite de lujo con sala de estar separada y vista panorámica de la ciudad.'
            },
            {
                'numero': '301',
                'tipo': 'familiar',
                'precio_por_noche': Decimal('200000'),
                'capacidad': 6,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar, cocina básica',
                'estado': 'disponible',
                'descripcion': 'Habitación familiar amplia con cocina básica, ideal para familias numerosas.'
            },
            {
                'numero': '401',
                'tipo': 'presidencial',
                'precio_por_noche': Decimal('500000'),
                'capacidad': 8,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar, jacuzzi, sala de estar, comedor, cocina completa, terraza privada',
                'estado': 'disponible',
                'descripcion': 'Suite presidencial de lujo con todas las comodidades y terraza privada.'
            },
            {
                'numero': '103',
                'tipo': 'individual',
                'precio_por_noche': Decimal('80000'),
                'capacidad': 1,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado',
                'estado': 'mantenimiento',
                'descripcion': 'Habitación individual en mantenimiento preventivo.'
            },
            {
                'numero': '203',
                'tipo': 'doble',
                'precio_por_noche': Decimal('120000'),
                'capacidad': 2,
                'servicios_incluidos': 'WiFi gratuito, TV cable, aire acondicionado, minibar',
                'estado': 'reservada',
                'descripcion': 'Habitación doble con reserva confirmada.'
            }
        ]
        
        habitaciones_creadas = 0
        habitaciones_existentes = 0
        
        for datos_habitacion in habitaciones_ejemplo:
            habitacion, created = Habitacion.objects.get_or_create(
                numero=datos_habitacion['numero'],
                defaults=datos_habitacion
            )
            
            if created:
                habitaciones_creadas += 1
                self.stdout.write(
                    f'✓ Habitación {habitacion.numero} creada: {habitacion.get_tipo_display()} - {habitacion.precio_formateado}'
                )
            else:
                habitaciones_existentes += 1
                self.stdout.write(
                    f'- Habitación {habitacion.numero} ya existe'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n¡Proceso completado!'
                f'\n- Habitaciones creadas: {habitaciones_creadas}'
                f'\n- Habitaciones que ya existían: {habitaciones_existentes}'
                f'\n- Total de habitaciones en el sistema: {Habitacion.objects.count()}'
            )
        ) 