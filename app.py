"""Ventana de escritorio. React solo presenta; Python procesa las operaciones."""
import os
import sys
from pathlib import Path
from api import API

def carpeta_datos():
    configurada = os.environ.get('HOTEL_DATA_DIR')
    if configurada:
        return Path(configurada)
    return Path(os.environ.get('LOCALAPPDATA',str(Path.home()))) / 'SistemaReservasHotel'

def bloquear(carpeta):
    import msvcrt
    carpeta.mkdir(parents=True,exist_ok=True)
    archivo = (carpeta / 'instancia.lock').open('a+b')
    archivo.seek(0,2)
    if archivo.tell() == 0:
        archivo.write(b'0')
        archivo.flush()
    archivo.seek(0)
    try:
        msvcrt.locking(archivo.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:
        archivo.close()
        raise ValueError('El sistema ya está abierto. Usa la ventana existente.')
    return archivo

def main():
    import webview
    carpeta = carpeta_datos()
    bloqueo = None
    try:
        bloqueo = bloquear(carpeta)
        api = API(carpeta)
        base = Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))
        interfaz = base / 'frontend' / 'build-ui' / 'index.html'
        if not interfaz.exists():
            raise ValueError('Falta construir la interfaz. Ejecuta PREPARAR.bat primero.')
        ventana = webview.create_window('Sistema de Gestión de Reservas de Hotel',str(interfaz),js_api=api,width=1200,height=760,min_size=(900,560),maximized=True,background_color='#F6F7FA')
        api._ventana = ventana
        webview.start(gui='edgechromium',debug=False)
    except Exception as error:
        import tkinter as tk
        from tkinter import messagebox
        raiz = tk.Tk();raiz.withdraw()
        messagebox.showerror('No se pudo iniciar',str(error))
        raiz.destroy()
        return 1
    finally:
        if bloqueo:
            bloqueo.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
