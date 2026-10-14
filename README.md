# 🏨 Sistema de Gestión de Reservas de Hotel

**Una aplicación de escritorio para organizar el trabajo de recepción.**

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![React 19](https://img.shields.io/badge/React-19-149ECA?logo=react&logoColor=white)
![Plataforma Windows](https://img.shields.io/badge/Plataforma-Windows-0078D4)

Reservas, huéspedes, habitaciones y pagos en un mismo lugar. Desarrollado como proyecto de **Estructura de Datos y Algoritmos**, con lógica en Python y una interfaz React dentro de una ventana de escritorio.

[Empezar](#empezar) · [Funciones](#funciones) · [Estructuras y algoritmos](#estructuras-y-algoritmos) · [Pruebas](#pruebas)

---

## El recorrido de una estadía

**Reservar → Recibir al huésped → Finalizar estadía → Limpieza → Habitación lista**

1. **Reservar.** Ingresar el DNI, elegir habitación y fechas, revisar el total y confirmar. Si el huésped ya está registrado, se recupera su nombre; si es nuevo, se guarda junto con la reserva.
2. **Recibir.** Registrar la llegada con un clic. La fecha debe corresponder a la estadía y la habitación debe estar lista.
3. **Cobrar.** Registrar abonos o el saldo completo. Los pagos pueden hacerse antes o durante la estadía; la salida requiere saldo cero.
4. **Finalizar.** Registrar el checkout. La habitación pasa a **Pendiente de limpieza** y se abre la sección Habitaciones.
5. **Limpiar.** Pulsar **Limpieza** inicia una simulación de **0 a 5 segundos**. Al terminar, la habitación queda lista para recibir al siguiente huésped.

Las reservas siguientes se conservan. Una habitación lista puede seguir apareciendo **Reservada** si ya tiene una llegada prevista.

## Funciones

| Sección | Qué permite hacer |
| --- | --- |
| **Recepción** | Buscar por nombre, DNI o habitación; filtrar reservas; ordenar por llegada o importe; recibir, cobrar, cancelar y finalizar estadías. |
| **Habitaciones** | Registrar número, tipo, capacidad y tarifa; consultar el estado; reservar e iniciar limpieza o mantenimiento. |
| **Huéspedes** | Registrar y consultar personas, identificadas por un DNI único de ocho dígitos. |
| **Cobros** | Consultar pagos registrados en soles, con métodos Efectivo, Tarjeta, Yape o Transferencia. |
| **Espera** | Guardar solicitudes sin habitación asignada y atender primero la más antigua. Una asignación fallida conserva el turno. |
| **Reportes** | Consultar ingresos según fecha de pago y reservas/noches según fecha de llegada. |
| **Historial** | Revisar las acciones registradas y recorrerlas en ambos sentidos. |
| **Datos** | Exportar e importar copias JSON y cargar un ejemplo ficticio cuando todavía no existen registros operativos. |

### Disponibilidad y trabajos simulados

- **Disponible hoy** indica que la habitación está libre para hoy. Si existe una reserva futura, se muestra su próxima fecha. Al reservar se comprueba todo el intervalo solicitado.
- **Limpiando** muestra un contador ascendente de **0 a 5 segundos**. Durante ese tiempo no se puede recibir al huésped; sí se pueden registrar reservas para fechas libres.
- **En mantenimiento** muestra un contador de **0 a 15 segundos**. Bloquea reservas y llegadas hasta terminar. No puede iniciarse si la habitación tiene reservas vigentes.

Ambos trabajos terminan automáticamente, simulando el aviso de otro departamento. Su hora de inicio se guarda: cambiar de pantalla no reinicia el cronómetro y, al reabrir la aplicación, se reconoce el tiempo transcurrido. No hay una conexión real con un sistema de personal.

### Validaciones principales

El sistema rechaza fechas de entrada pasadas, estadías de menos de una noche o más de 365, reservas solapadas, exceso de capacidad, DNI duplicados y pagos superiores al saldo. Una reserva con pagos no puede cancelarse, porque esta versión no gestiona reembolsos.

## Empezar

### Requisitos

- Windows con **Microsoft Edge WebView2 Runtime** disponible.
- **Python 3.12** y **Node.js 22.12 o superior**, accesibles desde la terminal.
- Internet para descargar las dependencias durante la preparación inicial.

### Preparar y abrir

Clonar el repositorio y preparar la aplicación:

```powershell
git clone https://github.com/Daniellaln/sistema-reservas-hotel.git
cd sistema-reservas-hotel
.\PREPARAR.bat
```

Cuando termine la preparación, abrir:

```powershell
.\ABRIR.bat
```

También se pueden ejecutar los archivos `.bat` con doble clic. **PREPARAR.bat** crea el entorno virtual, instala las dependencias y construye la interfaz. Después basta con **ABRIR.bat**; la aplicación funciona sin Internet.

Para explorarla, entrar en **Más → Datos → Cargar ejemplo**. El ejemplo usa huéspedes ficticios y fechas calculadas desde el día actual.

## Estructuras y algoritmos

Python concentra las reglas de negocio, las estructuras del curso y el almacenamiento. React presenta los datos y permite interactuar con ellos mediante **pywebview**.

| Implementación | Uso en el proyecto |
| --- | --- |
| **Listas de Python** | Colecciones de huéspedes, habitaciones, reservas y pagos. |
| **Cola simplemente enlazada, FIFO** | Solicitudes de espera: primero en entrar, primero en atender. |
| **Lista doblemente enlazada** | Historial con recorrido en ambos sentidos. |
| **Árbol binario de búsqueda** | Índice de huéspedes por DNI. Es un árbol normal, sin balanceo automático. |
| **Merge Sort recursivo y estable** | Ordenar reservas por llegada o importe. |
| **Recorridos y comparaciones de intervalos** | Buscar registros, comprobar disponibilidad, calcular saldos y finalizar trabajos simulados. |
| **Excepciones y archivos JSON** | Validar operaciones, conservar información y manejar fallos de lectura o escritura. |

Las estructuras enlazadas, el árbol y Merge Sort están implementados en el proyecto. [CURSO.md](CURSO.md) explica sus operaciones, pseudocódigo y complejidad.

## Datos y respaldo

Los datos se guardan fuera del repositorio:

```text
%LOCALAPPDATA%\SistemaReservasHotel\
├── hotel.json
├── hotel.anterior.json
└── instancia.lock
```

**hotel.json** contiene los registros actuales y **hotel.anterior.json** conserva la versión anterior al último guardado. La escritura utiliza un archivo temporal; las importaciones comprueban identificadores, referencias, fechas, solapamientos y saldos.

Desde **Más → Datos** se pueden exportar e importar copias. La aplicación impide abrir dos instancias sobre la misma carpeta de datos. Para pruebas se puede elegir una carpeta diferente con la variable `HOTEL_DATA_DIR`.

## Pruebas

```powershell
.\PROBAR.bat
```

La suite incluye **50 pruebas** de estructuras, reservas, pagos, estados, persistencia y cronómetros. Comprueba también que una asignación fallida conserve la cola, que no se dupliquen operaciones y que un error de guardado restaure el estado anterior.

Los recorridos de ventana y las comprobaciones previas a publicar están documentados en [PRUEBAS_MANUALES.md](PRUEBAS_MANUALES.md).

<details>
<summary><strong>Organización del código</strong></summary>

| Archivo o carpeta | Responsabilidad |
| --- | --- |
| `estructuras.py` | Nodos, cola enlazada, lista doble y árbol binario. |
| `algoritmos.py` | Merge Sort. |
| `modelo.py` | Reglas del hotel, estados y trabajos simulados. |
| `repositorio.py` | Validación y almacenamiento JSON. |
| `api.py` | Operaciones de la interfaz, reportes y actualización de cronómetros. |
| `app.py` | Ventana de escritorio, carpeta de datos y bloqueo de instancias. |
| `frontend/` | Interfaz React, estilos y configuración de construcción. |
| `tests/` | Pruebas automatizadas de Python. |

</details>

## Alcance

Prototipo académico para **un equipo y un operador**. No incluye facturación fiscal, reembolsos, edición de entidades, usuarios/permisos ni trabajo simultáneo desde varias computadoras. Las reservas y solicitudes vencidas se gestionan manualmente; una salida anticipada no recalcula el importe. Las estadías se manejan por fechas, sin horarios ni tarifas por horas.

Limpieza y mantenimiento son simulaciones breves para demostrar el flujo. Si una habitación tenía limpieza pendiente antes del mantenimiento, esa limpieza seguirá pendiente al finalizar la reparación.

La distribución como `.exe` es un paso posterior; este repositorio contiene el código fuente. [RELEASE.md](RELEASE.md) describe las comprobaciones previstas para el empaquetado.

---

**Más información:** [Guía de uso](GUIA_USO.md) · [Estructuras y algoritmos](CURSO.md) · [Diseño](DESIGN.md) · [Componentes de terceros](TERCEROS.md)

La interfaz utiliza [liquid-glass-react](https://github.com/rdev/liquid-glass-react) para la navegación. Su licencia se conserva en [LICENCIA_LIQUID_GLASS.txt](LICENCIA_LIQUID_GLASS.txt).
