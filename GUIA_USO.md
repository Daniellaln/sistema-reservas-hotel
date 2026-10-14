# Guía breve de recepción

| Sección | Para qué sirve |
| --- | --- |
| Recepción | Buscar reservas, recibir huéspedes, cobrar, ver detalles y finalizar estadías. |
| Habitaciones | Consultar capacidad y tarifa, reservar y simular limpieza o mantenimiento. Disponible hoy puede tener reservas futuras; la próxima fecha se muestra. |
| Huéspedes | Registrar personas y buscar por DNI. Una reserva también permite registrar a una persona nueva sin salir del formulario. |
| Cobros | Consultar los pagos ya registrados. Registrar un pago desde una reserva o mediante la acción de cobro. |
| Espera | Guardar solicitudes que aún no tienen habitación asignada: huésped, fechas y personas. Atiende primero la solicitud más antigua. |
| Reportes | Consultar ingresos según fecha de pago, y reservas/noches según fecha de llegada. |
| Historial | Consultar las acciones registradas y alternar el recorrido del historial. |
| Datos | Exportar copias JSON, importar copias válidas y cargar datos ficticios para demostración cuando el sistema está vacío. |

## Cómo funciona Espera

Primero debe estar registrado el huésped. Añadir solicitud guarda sus fechas y cantidad de personas. Cuando hay una habitación adecuada, Asignar habitación intenta convertir la primera solicitud en reserva; solo la retira de la cola si la asignación funciona. Si no hay disponibilidad, conserva el turno. Retirar primero permite descartar la primera solicitud con confirmación.

Es una cola enlazada FIFO: primero en entrar, primero en salir. No representa automáticamente la fila física de personas en recepción y no envía avisos ni asigna habitaciones por sí sola. Las solicitudes vencidas se revisan manualmente.


## Limpieza simulada

Confirmar el checkout abre Habitaciones y deja la habitación Pendiente de limpieza. Pulsar Limpieza inicia un cronómetro ascendente de 0 a 5 segundos con el estado Limpiando. Al terminar, Python registra la limpieza completada y habilita la recepción automáticamente; no hay botón Marcar lista.

La reserva siguiente se conserva. Mientras se limpia pueden crearse reservas para intervalos libres, pero Recibir está bloqueado. Al terminar puede aparecer Disponible hoy o Reservada, según el calendario.

## Mantenimiento simulado

Pulsar Mantenimiento y confirmar inicia el cronómetro de 0 a 15 segundos. En mantenimiento bloquea reservas y llegadas. Al terminar se habilita automáticamente, sin botón Habilitar. No se inicia si hay reservas vigentes; esto evita romper compromisos ya registrados.

La terminación simula el aviso de otro equipo de trabajo. No existe todavía un sistema conectado de limpieza o reparaciones. Si antes del mantenimiento había limpieza pendiente, seguirá pendiente y deberá ejecutarse su simulación de 5 segundos.

## Continuidad

La hora de inicio y duración se guardan en JSON. Cambiar de pantalla no reinicia el trabajo. Al reabrir, el sistema reconoce el tiempo transcurrido y finaliza los trabajos cuyo plazo ya pasó. Se impide iniciar dos trabajos simultáneos en la misma habitación.


