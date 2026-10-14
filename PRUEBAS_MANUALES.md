# Resultado de revisión y comprobaciones pendientes

## Verificado en ventana Windows

Datos ficticios aislados en HOTEL_DATA_DIR, sin modificar datos reales.

- [x] Apertura, navegación y paneles de recepción.
- [x] Registrar huésped, crear reserva y comprobar cotización: 2 noches × S/130 = S/260.
- [x] Abono S/10.25 y saldo S/249.75; rechazo de S/5000 sin limpiar el formulario.
- [x] Check-in; bloqueo de salida con deuda; cobro restante y check-out.
- [x] Reporte S/260, dos pagos, una llegada y dos noches.
- [x] Exportar e importar JSON mediante diálogos de Windows, conservando el contenido.
- [x] Invertir historial; cerrar y reiniciar sin perder pagos ni estados.
- [x] Buscar DNI con el árbol binario.
- [x] Crear solicitud de espera, asignar habitación y retirar el turno atendido.
- [x] Cancelar reserva sin pagos, conservando registros y pagos previos.
- [x] Ordenar por importe: S/160 antes que S/260.
- [x] Apertura maximizada; controles del panel visibles.
- [x] Tab/Shift+Tab permanecen en el panel y Escape lo cierra.
- [x] Reserva cancelada muestra Sin saldo exigible en la interfaz corregida.

## Pruebas Python

42 pruebas aprobadas: estructuras, homónimos, duplicados, fechas, solapamientos, capacidad, importes, estados, mantenimiento, asignación fallida que conserva la cola, ordenamiento, archivos dañados, fallos de escritura, importación inválida, dobles envíos y bloqueo de otra instancia. React se construye correctamente.

## Pendiente antes de release

- [ ] Preparar desde cero en otro Windows.
- [ ] Empaquetar ejecutable y probarlo sin Python ni Node, con WebView2.
- [ ] Verificar actualización y persistencia del paquete en ese equipo.

La revisión visual previa pendiente por expiración del permiso ya se realizó. Esto no garantiza ausencia absoluta de errores ni certifica uso comercial. El siguiente paso es empaquetar y probar el ejecutable para v1.0.0.



## Revisión de recepción rápida — entrega 09

- [x] Recibir un huésped con un clic: Confirmada → En estancia; siguiente acción Cobrar.
- [x] Escribir DNI existente y recuperar nombre, guardando otra reserva sin duplicar al huésped.
- [x] Reservar desde Habitaciones con habitación preseleccionada y cotización inicial de una noche.
- [x] Registrar DNI/nombre nuevo y reserva en una sola confirmación: tres huéspedes y tres reservas después de la prueba.
- [x] Habitación reservada para hoy aparece Reservada; regresión Python añadida.
- [x] Cotización bloquea la confirmación de un intervalo no disponible; Python vuelve a validar al guardar.
- [x] Cabecera integrada; botones verde y rojo restauran/maximizan y cierran la ventana.
- [x] Formulario de 500 px, campos de 17 px, total y confirmar visibles en una ventana de 1200 × 760.

42 pruebas Python aprobadas y construcción React exitosa. Capturas de pantalla reales con datos ficticios. No se ha realizado una medición de tiempos con recepcionistas ni una prueba de carga representativa.

## Revisión de menú, material y ventana — entrega 10

- [x] Más se cierra al hacer clic fuera; el panel se dibuja fuera del filtro de refracción.
- [x] Habitaciones muestra Disponible hoy y la fecha de la próxima reserva futura.
- [x] Mantenimiento se muestra deshabilitado para habitaciones con reservas vigentes.
- [x] Barra nativa de Windows restaurada; arrastre real comprobado mediante cambio de posición de ventana.
- [x] Elasticidad del componente restaurada; CSS conserva sus transforms y reflejos direccionales. Movimiento reducido según preferencia del sistema.

43 pruebas Python aprobadas, incluida la explicación de mantenimiento bloqueado por una reserva futura. Construcción React exitosa. No se ha empaquetado un ejecutable.

- [x] Escape cierra Más y devuelve el foco al botón.
- [x] Modo shader revisado en WebView2: eliminada la banda gris; reflejos y elasticidad permanecen activos.

## Verificación de limpieza — entrega 11

- [x] Finalizar estadía pagada marca Pendiente de limpieza y conserva la reserva de la llegada siguiente.
- [x] La llegada muestra Ver limpieza y abre Habitaciones directamente.
- [x] Marcar lista guarda limpieza completada; la habitación aparece Reservada cuando hay una reserva vigente.
- [x] Recibir vuelve a estar disponible; el siguiente huésped entra sin perder su reserva.
- [x] Persistencia JSON e historial conservan salida, limpieza y llegada.

47 pruebas Python aprobadas y construcción React exitosa. Flujo completo comprobado en Windows con datos ficticios aislados.
