# Diseño y uso en recepción

Una ventana continua, sin tarjetas para cada dato. La tabla usa filas y separadores; números de habitación y estados no se encierran en cápsulas. La navegación flotante usa liquid-glass-react 1.1.1 con refracción, transparencia y borde iluminado sobre un fondo con variación de color. El editor usa vidrio esmerilado. Se prioriza el contraste en los datos: vidrio para navegación, superficie clara para lectura.

La ventana tiene cabecera integrada y controles funcionales de cerrar, minimizar y restaurar/maximizar. El nombre Hotel permite arrastrar la ventana cuando está restaurada. Diseño inspirado en macOS y Linear; renderizado en Windows mediante WebView2.

Texto operativo de 16–18 px, nombres de 18 px, habitaciones de 19 px; objetivos principales de al menos 44 px. Etiquetas de tabla de 14 px. No reducir texto para hacer caber más reservas: se desplaza la lista. Preferencias de movimiento reducido, transparencia reducida y contraste elevado atendidas.

## Recorridos

- Con reserva: buscar nombre/DNI/habitación y pulsar Recibir. Cambia a En estancia sin confirmación adicional; la acción pasa a Cobrar si existe deuda.
- Sin reserva: Nueva reserva → DNI → nombre si es nuevo → habitación → confirmar. Hoy, mañana y una persona son valores iniciales editables. Un DNI existente recupera el nombre sin registrar otro huésped.
- Desde Habitaciones: Reservar abre el formulario con esa habitación elegida. La cotización comprueba las fechas; Disponible indica que la habitación está libre para hoy; Reservada indica que una reserva bloquea hoy. La cotización vuelve a validar todo el intervalo elegido.
- Cobrar: acción junto a la reserva, importe inicial igual al saldo; admite abonos y rechaza sobrepagos.

El huésped nuevo y la reserva se guardan juntos mediante una operación Python. Si falla la reserva o el guardado, no queda un huésped suelto. El foco inicia en el DNI; Tab recorre los campos, Enter envía el formulario y Escape cierra el editor. Cancelar y finalizar mantienen confirmación. Las funciones menos frecuentes permanecen en Más.

El total y la confirmación quedan fuera del área desplazable de campos. La ventana se abre maximizada; en pantallas pequeñas se desplazan los campos sin esconder la acción de guardar. No se prometen tiempos de atención medidos: deben probarse con usuarios y un volumen representativo de reservas.

