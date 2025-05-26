## 2.1 Perspectiva del Producto
La _ReservaFácil_ es un producto nuevo, diseñado como un sistema independiente y autoconclusivo. No forma parte de una familia de productos existente, ni es una actualización o reemplazo de otro sistema previo.

Este producto tiene como objetivo cubrir de manera integral el proceso de consulta de disponibilidad de habitaciones, creación de reservas, gestión de check-in y check-out, y envío de notificaciones relacionadas. Funciona como una solución completa, sin depender de la integración con otros sistemas externos, más allá del necesario para envío de correos de confirmación y facturación.

A continuación, se presenta un diagrama de alto nivel que ilustra los principales componentes del sistema y sus interacciones:  
![image](https://github.com/user-attachments/assets/92328906-fddc-449b-b915-793b33d0e336)

## 2.2 Funciones del Producto
![veggetaUml](https://github.com/user-attachments/assets/6b5d0215-a03b-4c88-aec5-5ed1eda2bd62)
### **1. Gestión de Habitaciones**
- **Consulta de disponibilidad por rango de fechas**  
  - Permitir a los clientes ingresar fechas de entrada y salida para consultar disponibilidad.  
  - Validar que la fecha de entrada sea anterior a la de salida y que ambas no sean anteriores al día actual.
- **Listado de habitaciones disponibles**  
  - Para cada habitación cuyo estado sea **Disponible** en todo el rango solicitado, mostrar:
    - Tipo de habitación (Individual, Doble, Suite, etc.)  
    - Precio por noche  
    - Características (servicios incluidos, tamaño, vistas, etc.)
- **Verificación de conflictos al confirmar reserva**  
  - Al confirmar la reserva, el sistema comprobará que no exista otra reserva confirmada para la misma habitación y fechas; de haber conflicto, notificará al usuario.

---

### **2. Gestión de Reservas**
- **Creación de reserva**  
  - El cliente deberá completar los campos obligatorios: identificación (nombre, correo electrónico), habitación seleccionada, fechas de entrada y salida.  
  - Validar que el correo tenga formato válido y que las fechas cumplan las reglas de negocio.
- **Generación de número de reserva único**  
  - Al crear la reserva, el sistema generará un número de reserva único y lo devolverá al usuario.
- **Envío de correo de confirmación**  
  - El sistema enviará un correo al cliente con:
    - Número de reserva  
    - Detalles de la habitación y fechas  
    - Información para consultar, modificar o cancelar la reserva desde su cuenta autenticada.

---

### **3. Gestión de Check-in y Check-out**
- **Check-in en línea**  
  - El sistema permitirá al cliente realizar el **check-in** en línea a partir de las 12:00 PM del día de llegada.  
  - Durante el check-in, el cliente confirmará datos personales (documento de identidad, teléfono de contacto).  
  - El sistema registrará fecha y hora exacta de check-in y cambiará el estado de la reserva a **En curso**.
- **Check-out en línea o en recepción**  
  - El cliente podrá gestionar el **check-out** en línea hasta las 12:00 PM del día de salida o directamente en recepción.  
  - Al hacer check-out, el sistema:
    - Registrará fecha y hora de salida.  
    - Calculará cargos adicionales (minibar, servicios extra) y presentará un resumen antes de finalizar el proceso.  
    - Cambiará el estado de la estancia a **Finalizada**.  
  - El sistema enviará una factura final al correo del cliente o la dejará disponible para recogerse en recepción.

---

### **4. Autenticación y Cuentas**
- **Registro de cuenta de cliente**  
  - Los clientes deben crear una cuenta con nombre, correo electrónico y contraseña antes de poder realizar cualquier reserva.  
  - La contraseña deberá cumplir con criterios mínimos de seguridad (longitud y complejidad).
- **Inicio de sesión**  
  - Los usuarios deberán autenticarse con correo electrónico y contraseña para:
    - Crear reservas  
    - Consultar, modificar o cancelar reservas existentes  
    - Realizar el check-in y check-out en línea  
    - Ver su historial de reservas  
  - Si un cliente introduce credenciales inválidas, el sistema mostrará un mensaje de error.

---

### **5. Administración (Back-Office)**
- **Gestión de habitaciones** (solo personal autorizado)  
  - CRUD de habitaciones (crear, editar, eliminar, listar).  
  - Definir atributos: tipo, precio por noche, servicios incluidos, capacidad, estado (Disponible, Mantenimiento, Reservada).
- **Gestión de reservas**  
  - Visualizar todas las reservas con filtros (fecha, estado, cliente, habitación).  
  - Modificar el estado de la reserva (por ejemplo, marcar como **Confirmada**, **Cancelada** o **En curso**) manualmente.
- **Informes y métricas**  
  - Ocupación diaria/mensual por tipo de habitación.  
  - Historial de cancelaciones.  
  - Reportes de ingresos (el detalle de ingresos se registrará en el sistema, aunque el cobro se realice en recepción).

## 2.3 Clases de Usuario y Características

El sistema _ReservaFácil_ está diseñado para ser utilizado por tres clases principales de usuarios, con diferentes privilegios y características:

### **1. Clientes (Usuarios Externos)**
- **Frecuencia de uso**: Moderada a alta.  
- **Funciones utilizadas**:  
  - Registro y autenticación de cuenta.  
  - Consulta de disponibilidad de habitaciones.  
  - Creación, modificación y cancelación de reservas.  
  - Check-in y check-out en línea.  
  - Consulta de historial de reservas y facturas.  
- **Nivel técnico**: Bajo a medio.  
- **Privilegios**:  
  - Acceso a su propio perfil y a la gestión completa de sus reservas.  
  - No puede ver ni modificar información de otros clientes.  

---

### **2. Personal de Recepción (Usuarios Internos)**
- **Frecuencia de uso**: Alta.  
- **Funciones utilizadas**:  
  - Autenticación en el sistema.  
  - Consulta y gestión de reservas (confirmar, cancelar o reasignar habitaciones).  
  - Gestión de check-in y check-out manual cuando el cliente se presenta en recepción.  
  - Registro de cargos adicionales (minibar, servicios extra).  
  - Emisión de facturas y comprobantes de pago en recepción.  
- **Nivel técnico**: Medio.  
- **Privilegios**:  
  - Acceso a todas las reservas del día y a la información de los clientes que vayan a hacer check-in/check-out.  
  - No puede crear ni eliminar cuentas de Administrador.  

---

### **3. Administrador (Usuario Interno con Privilegios Ampliados)**
- **Frecuencia de uso**: Alta.  
- **Funciones utilizadas**:  
  - Todas las funciones del Personal de Recepción.  
  - Creación, edición y eliminación de cuentas de Personal de Recepción.  
  - Configuración y mantenimiento de la base de datos de habitaciones.  
  - Generación de informes y métricas globales.  
- **Nivel técnico**: Medio-alto.  
- **Privilegios**:  
  - Acceso completo al sistema: gestión de habitaciones, reservas, usuarios internos e informes.  

### Resumen de Clases de Usuario

| **Clase de Usuario**             | **Frecuencia de Uso** | **Funciones Principales**                                                                                                                | **Nivel Técnico** | **Privilegios**                                                                                     |
|----------------------------------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------|-------------------|-----------------------------------------------------------------------------------------------------|
| **Clientes (Externos)**          | Moderada a Alta       | Registro y gestión de reservas, consultas de disponibilidad, check-in/check-out, consulta de historial y facturas                       | Bajo a Medio      | Acceso completo a su propio perfil y reservas                                                       |
| **Personal de Recepción**        | Alta                  | Gestión de reservas diarias, confirmación/cancelación, check-in/check-out manual, registro de cargos adicionales, emisión de facturas   | Medio             | Acceso a información de reservas diarias y facturación; no gestión de usuarios internos            |
| **Administrador (Interno)**      | Alta                  | Todas las funciones de Personal de Recepción, más gestión de usuarios internos, configuración de habitaciones, informes                  | Medio-Alto        | Acceso completo a habitaciones, reservas, usuarios internos e informes                              |

---

## 2.5 Restricciones de Diseño e Implementación
- **Arquitectura**:  
  Basada en el patrón **Modelo-Vista-Template (MVT)** de **Django**, independiente y RESTful para APIs internas.
- **Lenguaje y Framework**:  
  Backend y lógica de negocio implementados con **Python** y **Django**.  
  Frontend usando **Django Templates** y, de ser necesario, **AJAX** para interacciones dinámicas.
- **Base de datos**:  
  SQLite (archivo local) para prototipado y despliegue inicial.
- **Autenticación y autorización**:  
  Gestionadas con el sistema de **auth** de Django (usuarios, grupos y permisos).  
  Sesiones y contraseñas cifradas según estándares de Django.
- **Envió de correos**:  
  Integración con el backend de correos de Django (`EMAIL_BACKEND`) para confirmaciones, notificaciones de check-in/check-out y facturas.
- **Validaciones**:  
  Formularios de Django (`ModelForm` y `Form`) para validación en servidor; validación adicional en frontend con JavaScript si procede.
- **Seguridad**:  
  - Uso de **HTTPS** obligatorio.  
  - Control de acceso basado en permisos de Django (roles Cliente, Recepción, Administrador).  
  - Cifrado de contraseñas y protección CSRF nativo de Django.

## 2.6 Documentación para el Usuario
- **Tutoriales en línea**:  
  Videos y guías paso a paso para:
  - Registro de cuenta y autenticación.  
  - Consulta de disponibilidad y gestión de reservas.  
  - Proceso de check-in y check-out.
- **Soporte en línea**:  
  Chat integrado y sistema de tickets por correo.
- **Manuales de usuario (PDF)**:  
  - Cliente: registro, reserva, modificación y check-in/out.  
  - Personal de Recepción: gestión diaria y facturación.  
  - Administrador: configuración de sistema y generación de informes.

## 2.7 Supuestos y Dependencias

### Supuestos
- Clientes con acceso a Internet y conocimientos básicos de web.  
- Entorno de servidor compatible con Python, Django y SQLite.  
- Cuenta activa de correo configurada en Django.

### Dependencias
- **Django** y librerías oficiales (Rest Framework si se extiende API).  
- Servicio de correo SMTP configurado.  
- Navegadores modernos compatibles con HTML5 y ECMA-Script.


