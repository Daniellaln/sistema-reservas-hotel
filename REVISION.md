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
