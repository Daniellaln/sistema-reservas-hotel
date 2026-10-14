# Revisión de la aplicación

Resultado: flujo principal comprobado en la ventana Windows, 39 pruebas Python aprobadas y construcción React correcta. Se utilizaron registros ficticios en una carpeta de datos separada.

## Correcciones

1. La altura inicial de la ventana dejaba el pie del editor fuera de la pantalla. Ahora inicia maximizada y admite un tamaño mínimo menor.
2. Se restringió el foco al panel abierto mediante inert y ciclo de Tab/Shift+Tab. Escape en una confirmación cierra la confirmación sin cerrar también el panel. El foco vuelve al control que abrió el editor.
3. Se exige formato de fechas AAAA-MM-DD para evitar comparar fechas compactas como 20261013 con fechas de formato distinto. También se valida en las copias importadas.
4. Las solicitudes importadas de espera respetan la duración máxima de 365 noches.
5. Se rechazan booleanos usados como versión de archivo o revisión de importación.
6. Una reserva cancelada conserva su importe histórico, pero la interfaz muestra “Sin saldo exigible” y no la suma a la deuda pendiente.

## Evidencia de flujo

Huésped ficticio Ana Prueba, DNI 20000001. Reserva en habitación 102 del 13 al 15 de octubre de 2026: S/260. Abono S/10.25; rechazo de S/5000; saldo S/249.75. Check-in aceptado; salida con deuda rechazada; cobro del resto; salida finalizada. Reporte con dos pagos y S/260. Copia JSON exportada e importada sin perder información. Reinicio conserva el estado. Solicitud en cola atendida en habitación 201 por S/160, después cancelada sin borrar la reserva.

## Límites

Prototipo académico de una computadora y un operador. No hay reembolsos, facturación fiscal, edición de registros ni acceso compartido. La cancelación con pagos está bloqueada. El ejecutable aún no se ha generado ni probado en un Windows limpio. Las entregas previas permanecen como etapas históricas; esta corrección se entrega como commit 08.

## Entrega 09: interfaz y recepción rápida

Se sustituyó la composición de tarjetas por una ventana continua con tabla y separadores. Navegación liquid-glass-react, editor esmerilado y cabecera integrada; textos operativos de 16–18 px. Reserva y huésped se guardan juntos; DNI conocido recupera el nombre, una noche es el valor inicial y Recibir actúa con un clic. El registro correcto vuelve a Recepción y despeja la búsqueda para mostrar la reserva. La disponibilidad actual distingue Reservada y se valida nuevamente para el intervalo.

42 pruebas Python aprobadas, construcción React y recorridos con datos ficticios en Windows comprobados. El .exe y la revisión en otro Windows siguen pendientes.

## Entrega 10

Se restauró la barra nativa de Windows. Más es un desplegable controlado en una capa independiente y se cierra al salir con el foco, pulsar fuera, Escape o elegir una sección. El vidrio utiliza el modo shader, elasticidad 0.25 y reflejos de liquid-glass-react; ya no se anulan sus transforms ni se aplica el filtro al menú. Se muestra Disponible hoy y la próxima reserva futura. Mantenimiento queda deshabilitado si hay reservas vigentes. GUIA_USO.md explica cada sección y el alcance de Espera.

43 pruebas Python aprobadas y construcción React exitosa. Arrastre nativo y cierre al pulsar fuera verificados en Windows.


## Entrega 11: limpieza

El checkout marca limpieza pendiente. El campo booleano se almacena en JSON y se valida; se aceptan copias anteriores sin el campo. Las reservas continúan, pero Python bloquea el check-in mientras la habitación esté pendiente. Habitaciones ofrece Marcar lista, y una llegada pendiente ofrece Ver limpieza. Mantenimiento sigue siendo un bloqueo independiente para reparaciones.

47 pruebas Python aprobadas, incluyendo salida con deuda, persistencia, conservación de reservas durante la limpieza, bloqueo de recepción, limpieza completada, compatibilidad de JSON antiguo y rechazo de estados incoherentes. Construcción React exitosa.


## Entrega 12: trabajos simulados con cronómetro

Limpieza inicia un contador de 0 a 5 segundos; Mantenimiento, de 0 a 15. Python valida el inicio, guarda inicio/duración, termina el trabajo y registra el evento. React muestra el avance y consulta el estado mientras hay trabajos. Terminar el checkout abre Habitaciones para iniciar Limpieza. No hay Marcar lista ni Habilitar manuales. Se conserva el calendario de reservas y no se permite recibir durante limpieza ni reservar en mantenimiento.

Los cronómetros sobreviven a cambios de pantalla y reapertura. No hay integración real con otro sistema de personal. Una limpieza pendiente anterior se conserva al terminar mantenimiento.

50 pruebas Python aprobadas: plazos exactos, bloqueo de acciones, trabajos duplicados, reinicio, formatos inválidos y restauración del estado si falla el guardado. Construcción React exitosa.
