# Sistema de Gestión de Reservas de Hotel

Proyecto académico de Estructura de Datos y Algoritmos. Conserva la idea original: registrar huéspedes, habitaciones, reservas, pagos y reportes para recepción. La implementación es nueva y no contiene código del repositorio del grupo.

Python ejecuta las reglas de negocio y las estructuras escritas desde cero. React presenta los formularios en una ventana de escritorio mediante pywebview. La interfaz no implementa las estructuras del curso.

Las entregas son copias completas y progresivas del proyecto. Consulta la guía fuera de la carpeta proyecto de cada entrega para el mensaje de commit y sus comprobaciones.

## Abrir en Windows

Para preparar el código fuente se necesita Python 3.12, Node.js 22.12 o superior y acceso a Internet para descargar dependencias. La ventana usa Microsoft Edge WebView2 Runtime, instalado normalmente en Windows actual. Si no está disponible, instalarlo desde Microsoft.

1. Copiar esta entrega completa al repositorio nuevo.
2. Ejecutar PREPARAR.bat una vez: crea .venv, instala Python y React y construye la interfaz.
3. Abrir ABRIR.bat.
4. Abrir PROBAR.bat para ejecutar las pruebas Python.

La aplicación funciona sin Internet una vez preparada. El código React es una presentación local; el procesamiento y almacenamiento están en Python. No se utiliza el código del repositorio anterior.

## Datos

Guardado en %LOCALAPPDATA%\SistemaReservasHotel\hotel.json, fuera de la carpeta del proyecto. Copia previa: hotel.anterior.json. Exportación e importación desde Datos. La aplicación impide abrir dos instancias con la misma carpeta de datos. HOTEL_DATA_DIR permite elegir una carpeta aislada para pruebas.

Para una demo, en Datos se puede cargar un ejemplo ficticio con dos huéspedes y reservas. Solo se permite cuando los registros están vacíos. Las fechas de ese ejemplo se calculan desde hoy.

## Archivos propios

- estructuras.py: nodos, cola, lista doble y árbol binario normal.
- algoritmos.py: Merge Sort propio.
- modelo.py: reglas del hotel.
- repositorio.py: JSON y validación de integridad.
- api.py: puente transaccional y reportes.
- app.py: ventana, ruta de datos y bloqueo de instancias.
- frontend/src/App.jsx y style.css: interfaz React.
- tests: casos de estructuras, negocio, persistencia y puente.

CURSO.md contiene las explicaciones para la sustentación. PRUEBAS_MANUALES.md registra lo que falta comprobar en la ventana antes de publicar. RELEASE.md prepara la futura release; todavía no se ha generado un .exe.

## Límites del prototipo

Un equipo y un operador. Sin facturación fiscal, reembolsos, edición de entidades ni usuarios/permisos. No es un sistema hotelero de producción. Las reservas vencidas y las solicitudes vencidas se gestionan manualmente; el check-out temprano no recalcula el total. El árbol no se equilibra automáticamente. Los JSON anteriores del prototipo Tkinter o JavaScript no se importan como parte de estas entregas. No introducir datos reales en una demostración de clase.

Documentación de las tecnologías: https://pywebview.flowrl.com/guide/interdomain.html y https://vite.dev/guide/.

## Recepción rápida (entrega 09)

Nueva reserva permite registrar al huésped y la reserva en un solo formulario. Escribir un DNI existente recupera el nombre; no hay que cambiar entre formularios. Los valores iniciales son entrada hoy, salida mañana y una persona. Revisarlos antes de guardar. Reservar desde Habitaciones preselecciona la habitación, y la cotización comprueba el intervalo solicitado.

Recibir cambia una reserva válida a En estancia directamente. La barra nativa de Windows permite mover, minimizar, restaurar/maximizar y cerrar. La navegación usa liquid-glass-react y la presentación concentra el vidrio en los controles. Consulta DESIGN.md y TERCEROS.md.

