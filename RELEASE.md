# Preparación para la futura release v1.0.0

Este documento prepara el siguiente paso. No hay ejecutable ni release publicada todavía.

1. Completar PRUEBAS_MANUALES.md y resolver cualquier defecto.
2. Ejecutar las pruebas Python y reconstruir React.
3. Instalar PyInstaller en el entorno virtual de construcción.
4. Empaquetar la ventana con los archivos frontend/build-ui. No incluir datos de huéspedes ni el archivo hotel.json.
5. Probar el paquete en otra carpeta y en un Windows limpio. La interfaz requiere Microsoft Edge WebView2 Runtime; no requiere Python o Node en el equipo del operador una vez empaquetada.
6. Comprobar que los datos se guardan en %LOCALAPPDATA%\SistemaReservasHotel y sobreviven al reemplazo de la aplicación.
7. Crear etiqueta v1.0.0 en el commit final y una release GitHub con el paquete Windows, guía de uso y cambios.

La guía paso a paso de compilación se hará después de revisar la aplicación, como acordamos. pywebview recomienda PyInstaller y añadir el directorio de la interfaz construida: https://pywebview.flowrl.com/guide/freezing.html
