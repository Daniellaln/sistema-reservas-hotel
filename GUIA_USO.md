# Guía breve de recepción

| Sección | Para qué sirve |
| --- | --- |
| Recepción | Buscar reservas, recibir huéspedes, cobrar, ver detalles y finalizar estadías. |
| Habitaciones | Consultar capacidad y tarifa, reservar y habilitar o bloquear por mantenimiento. Disponible hoy puede tener reservas futuras; la próxima fecha se muestra. |
| Huéspedes | Registrar personas y buscar por DNI. Una reserva también permite registrar a una persona nueva sin salir del formulario. |
| Cobros | Consultar los pagos ya registrados. Registrar un pago desde una reserva o mediante la acción de cobro. |
| Espera | Guardar solicitudes que aún no tienen habitación asignada: huésped, fechas y personas. Atiende primero la solicitud más antigua. |
| Reportes | Consultar ingresos según fecha de pago, y reservas/noches según fecha de llegada. |
| Historial | Consultar las acciones registradas y alternar el recorrido del historial. |
| Datos | Exportar copias JSON, importar copias válidas y cargar datos ficticios para demostración cuando el sistema está vacío. |

## Cómo funciona Espera

Primero debe estar registrado el huésped. Añadir solicitud guarda sus fechas y cantidad de personas. Cuando hay una habitación adecuada, Asignar habitación intenta convertir la primera solicitud en reserva; solo la retira de la cola si la asignación funciona. Si no hay disponibilidad, conserva el turno. Retirar primero permite descartar la primera solicitud con confirmación.

Es una cola enlazada FIFO: primero en entrar, primero en salir. No representa automáticamente la fila física de personas en recepción y no envía avisos ni asigna habitaciones por sí sola. Las solicitudes vencidas se revisan manualmente.

## Mantenimiento

El bloqueo es indefinido hasta volver a habilitar la habitación. Por eso no se permite bloquear una habitación con reservas vigentes, incluso si están previstas para otro día. La pantalla muestra la próxima reserva y deshabilita el botón para explicar esa restricción antes de intentar guardar.
