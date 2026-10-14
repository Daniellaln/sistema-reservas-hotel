# Revisión antes de presentar o publicar

Las pruebas Python no sustituyen esta revisión de la ventana. Usar datos ficticios y exportar una copia antes de importar.

- [ ] Preparar y abrir desde una carpeta nueva en Windows.
- [ ] Revisar agenda, huéspedes, habitaciones, cobros, espera, reportes, historial y datos.
- [ ] Registrar dos huéspedes homónimos con DNI distintos.
- [ ] Crear reserva para hoy, comprobar cotización y hacer check-in.
- [ ] Rechazar reserva solapada y aceptar entrada igual a salida de otra.
- [ ] Rechazar fechas pasadas, salida igual a entrada y cantidad excesiva.
- [ ] Registrar abono de S/10.25; rechazar un pago mayor que el saldo.
- [ ] Rechazar check-out con saldo; completar cobro y finalizar estancia.
- [ ] Cancelar una reserva sin pagos; bloquear cancelación con pagos.
- [ ] Añadir dos solicitudes de espera y atender la primera.
- [ ] Confirmar que una asignación fallida no retira la solicitud.
- [ ] Buscar DNI en árbol; ordenar agenda por fecha y por importe.
- [ ] Invertir historial y consultar reportes por período.
- [ ] Exportar JSON, cerrar y volver a abrir: datos conservados.
- [ ] Importar copia válida; rechazar JSON inválido sin reemplazar datos.
- [ ] Intentar abrir dos instancias: la segunda debe bloquearse.
- [ ] Revisar zoom del sistema, tabulación, Escape, paneles y mensajes.
- [ ] Probar el ejecutable empaquetado en un equipo limpio con WebView2.

Estado de esta entrega: las pruebas unitarias y de integración Python pasan; React se construye; la ventana inicia. La inspección visual automatizada no se completó por expiración del permiso de acceso a la ventana. La release v1.0.0 queda pendiente de esta revisión y de empaquetar/probar el ejecutable.
