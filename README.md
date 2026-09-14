# Mercado VIVA - Módulo Omnicanal de Devoluciones 

**Desarrolladores:** Miguel Angel Salazar y Jose Angel Sanchez
## Arquitectura del Sistema
Para entender cómo interactúan los componentes del MVP en tiempo real, desde el escaneo en la PWA hasta la validación en la base de datos, puedes consultar nuestro diagrama oficial:

 **[diagrama de arquitectura de software](https://app.eraser.io/workspace/PUJpmbxuyVwzQqDgqIMm?origin=share)**

 
 **[link de render para el front](https://mercado-viva-1.onrender.com/)**


 
 **[link del front para el back](https://mercado-viva-hfiu.onrender.com/)**

## Descripción del Proyecto
El objetivo principal de este MVP es solucionar la desconexión logística entre la tienda física y la plataforma digital al momento de procesar devoluciones. Mediante una plataforma web progresiva (PWA) con diseño espacial 3D, agilizamos el proceso para que el inventario se sincronice automáticamente en tiempo real, reduciendo la dependencia de procesos manuales y mejorando la experiencia del cliente.

## Actores del Sistema
* **Cliente:** Inicia el proceso presentando el ID o código QR de su pedido digital.
* **Cajero / Asesor:** Opera la plataforma en el punto de venta (POS) escaneando el código para procesar la transacción.
* **Sistema Central:** Valida las reglas de negocio, autoriza la devolución y actualiza el inventario central.

## Reglas de Negocio y Restricciones
* **Validación de estado:** El producto debe cumplir con los criterios de buen estado para poder regresar al inventario físico.
* **Bloqueo Antifraude:** La API verifica el estado de la compra en la nube para evitar que una misma factura sea devuelta dos veces.
* **Seguridad de Montos:** Las devoluciones que superan los $500.000 COP exigen un PIN de autorización de un supervisor en tiempo real.
* **Operación Continua:** El diseño respeta el presupuesto limitado utilizando los dispositivos actuales de la tienda sin interrumpir sus ventas diarias.

## Historias de Usuario Implementadas
* **Búsqueda de Pedidos:** El cajero puede escanear o teclear el ID del pedido y obtener instantáneamente los detalles del cliente y el monto total.
* **Aprobación y Sincronización:** Al aprobar una devolución por "buen estado", el inventario en la base de datos suma +1 automáticamente.
* **Notificaciones UI:** El sistema genera comprobantes visuales dinámicos integrados en el diseño holográfico para asegurar que el proceso fue exitoso.

## Stack Tecnológico y Requisitos No Funcionales
* **Frontend (Mantenibilidad):** PWA ligera con interfaz holográfica 3D (HTML, CSS, JavaScript) e integración de cámara mediante `html5-qrcode`.
* **Backend (Rendimiento):** Construido con FastAPI (Python) para procesar consultas a la base de datos con latencia mínima.
* **Base de Datos (Dato Único):** PostgreSQL alojado en Supabase, garantizando la sincronización absoluta entre la web y el mundo físico.
* **Seguridad:** Sistema de autenticación JWT para el control de acceso del personal autorizado.
