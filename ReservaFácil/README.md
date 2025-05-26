# ReservaFácil - Sistema de Reservas de Hotel

## Comandos de Gestión

### Crear Habitaciones de Ejemplo
Para crear habitaciones de ejemplo en el sistema, ejecuta:
```bash
python manage.py crear_habitaciones_ejemplo
```

Este comando creará 8 habitaciones de diferentes tipos y estados:
- 2 habitaciones individuales (101, 103)
- 2 habitaciones dobles (102, 203)
- 1 habitación matrimonial (201)
- 1 suite (202)
- 1 habitación familiar (301)
- 1 suite presidencial (401)

### Crear Perfiles Faltantes
Si necesitas crear perfiles de usuario para usuarios existentes que no tienen perfil:
```bash
python manage.py crear_perfiles_faltantes
```

## Estructura del Proyecto

### Aplicaciones
- `usuarios`: Gestión de usuarios y autenticación
- `habitaciones`: Gestión de habitaciones y disponibilidad
- `reservas`: Gestión de reservas (en desarrollo)
- `checkin_checkout`: Gestión de check-in/check-out (en desarrollo)

### Características Implementadas
- Sistema de autenticación completo
- Gestión de habitaciones (CRUD)
- Consulta de disponibilidad por fechas
- Interfaz moderna con Bootstrap 5
- Control de acceso basado en roles

## Requisitos
- Python 3.8+
- Django 5.0+
- Bootstrap 5
- Font Awesome 6

## Instalación
1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Aplicar migraciones: `python manage.py migrate`
6. Crear superusuario: `python manage.py createsuperuser`
7. Crear habitaciones de ejemplo: `python manage.py crear_habitaciones_ejemplo`
8. Ejecutar servidor: `python manage.py runserver` 