"""Puente de la interfaz: cada modificación se valida y guarda en Python."""
from copy import deepcopy
from threading import RLock
from pathlib import Path
import json
from datetime import date, timedelta
from modelo import Hotel
from algoritmos import merge_sort
from repositorio import Repositorio, validar

class API:
    def __init__(self, carpeta, reloj=date.today):
        self._repo = Repositorio(carpeta)
        self._reloj = reloj
        self._hotel = Hotel(self._repo.leer(),reloj)
        self._lock = RLock()
        self._revision = 0
        self._orden = 'entrada'
        self._ventana = None

    def _estado(self, orden=None):
        if orden == None:
            orden = self._orden
        if orden not in ['entrada','total']:
            raise ValueError('Orden inválido.')
        d = deepcopy(self._hotel.datos)
        reservas = merge_sort(d['reservas'],orden)
        ingresos = 0
        pendiente = 0
        abiertas = 0
        llegadas = 0
        for r in reservas:
            r['nombre'] = self._hotel.indice.buscar(r['dni'])['nombre']
            r['saldo'] = self._hotel.saldo(r['id'])
            r['noches'] = (date.fromisoformat(r['salida'])-date.fromisoformat(r['entrada'])).days
            if r['estado'] in ['Confirmada','En estancia']:
                pendiente = pendiente + r['saldo']
            if r['estado'] == 'En estancia':
                abiertas = abiertas + 1
            if r['estado'] == 'Confirmada' and r['entrada'] == self._reloj().isoformat():
                llegadas = llegadas + 1
        for p in d['pagos']:
            ingresos = ingresos + p['monto']
            r = self._hotel.obtener(p['reserva'])
            p['nombre'] = self._hotel.indice.buscar(r['dni'])['nombre']
        for h in d['habitaciones']:
            h['estado'] = 'Disponible'
            if h['mantenimiento']:
                h['estado'] = 'Mantenimiento'
            elif self._hotel.tiene_estancia(h['numero']):
                h['estado'] = 'Ocupada'
        for i,s in enumerate(d['espera']):
            s['orden'] = i+1
            s['nombre'] = self._hotel.indice.buscar(s['dni'])['nombre']
        d['reservas'] = reservas
        d['historial'] = self._hotel.historial.listar(True)
        d['revision'] = self._revision
        d['hoy'] = self._reloj().isoformat()
        d['resumen'] = {'ingresos':ingresos,'pendiente':pendiente,'abiertas':abiertas,'llegadas':llegadas}
        return d

    def estado(self, orden='entrada'):
        with self._lock:
            datos = self._estado(orden)
            self._orden = orden
            return datos

    def _texto(self, datos, clave, maximo=200):
        valor = datos.get(clave,'')
        if not isinstance(valor,str) or len(valor)>maximo:
            raise ValueError('Campo inválido: '+clave)
        return valor.strip()

    def _numero(self, datos, clave):
        valor = datos.get(clave,'')
        if isinstance(valor,bool):
            raise ValueError('Cantidad inválida.')
        texto = str(valor)
        if not texto.isascii() or not texto.isdigit():
            raise ValueError('Cantidad inválida: '+clave)
        return int(texto)

    def _modificar(self, accion, d):
        h = self._hotel
        texto = lambda k:self._texto(d,k)
        if accion == 'huesped':
            h.huesped(texto('dni'),texto('nombre'),texto('telefono'))
        elif accion == 'habitacion':
            h.habitacion(texto('numero'),texto('tipo'),self._numero(d,'capacidad'),texto('tarifa'))
        elif accion == 'reserva':
            h.reserva(texto('dni'),texto('numero'),texto('entrada'),texto('salida'),self._numero(d,'personas'))
        elif accion == 'pago':
            h.pago(texto('id'),texto('monto'),texto('metodo'))
        elif accion == 'estado':
            h.estado(texto('id'),texto('estado'))
        elif accion == 'mantenimiento':
            h.mantenimiento(texto('numero'))
        elif accion == 'espera':
            h.esperar(texto('dni'),texto('entrada'),texto('salida'),self._numero(d,'personas'))
        elif accion == 'atender':
            h.atender(texto('numero'))
        elif accion == 'retirar':
            h.retirar_espera()
        elif accion == 'demo':
            if len(h.datos['huespedes']) or len(h.datos['reservas']) or len(h.datos['pagos']) or len(h.datos['espera']):
                raise ValueError('El ejemplo solo puede cargarse con los registros vacíos.')
            hoy = self._reloj()
            h.huesped('10000001','Valeria Torres','900000001')
            h.huesped('10000002','Mateo Salazar','900000002')
            h.reserva('10000001','101',hoy.isoformat(),(hoy+timedelta(days=2)).isoformat(),1)
            h.reserva('10000002','102',(hoy+timedelta(days=1)).isoformat(),(hoy+timedelta(days=4)).isoformat(),2)
        else:
            raise ValueError('Operación no reconocida.')

    def operar(self, accion, datos, revision):
        with self._lock:
            antes = deepcopy(self._hotel.datos)
            try:
                if type(revision) != int or revision != self._revision:
                    raise ValueError('La información cambió. Actualiza la vista antes de guardar otra vez.')
                if not isinstance(datos,dict):
                    raise ValueError('Datos inválidos.')
                self._modificar(accion,datos)
                self._repo.guardar(self._hotel.datos)
                self._revision = self._revision+1
                return {'ok':True,'mensaje':'Cambios guardados.','datos':self._estado()}
            except (ValueError,TypeError,KeyError,OSError) as error:
                self._hotel = Hotel(antes,self._reloj)
                return {'ok':False,'mensaje':str(error),'datos':self._estado()}

    def cotizar(self, numero, entrada, salida, personas):
        with self._lock:
            try:
                h = self._hotel.buscar_habitacion(numero)
                if h == None:
                    raise ValueError('Selecciona una habitación.')
                noches = self._hotel.rango(entrada,salida)
                cantidad = self._numero({'personas':personas},'personas')
                if not 1 <= cantidad <= h['capacidad']:
                    raise ValueError('La cantidad excede la capacidad.')
                return {'ok':True,'noches':noches,'total':noches*h['tarifa'],'disponible':self._hotel.disponible(numero,entrada,salida)}
            except (ValueError,TypeError) as error:
                return {'ok':False,'mensaje':str(error)}

    def buscar(self, dni):
        with self._lock:
            return deepcopy(self._hotel.indice.buscar(dni))

    def reportes(self, entrada, salida):
        with self._lock:
            try:
                a = date.fromisoformat(entrada)
                b = date.fromisoformat(salida)
                if b < a:
                    raise ValueError('El final del reporte debe ser igual o posterior al inicio.')
                ingresos = 0
                pagos = 0
                reservas = 0
                noches = 0
                for pago in self._hotel.datos['pagos']:
                    dia = date.fromisoformat(pago['fecha'][:10])
                    if a <= dia <= b:
                        ingresos = ingresos + pago['monto']
                        pagos = pagos + 1
                for r in self._hotel.datos['reservas']:
                    if r['estado'] != 'Cancelada' and entrada <= r['entrada'] <= salida:
                        reservas = reservas + 1
                        noches = noches + (date.fromisoformat(r['salida'])-date.fromisoformat(r['entrada'])).days
                return {'ok':True,'ingresos':ingresos,'pagos':pagos,'reservas':reservas,'noches':noches}
            except (ValueError,TypeError) as error:
                return {'ok':False,'mensaje':str(error)}

    def exportar(self):
        import webview
        with self._lock:
            try:
                rutas = self._ventana.create_file_dialog(webview.FileDialog.SAVE,save_filename='hotel-'+self._reloj().isoformat()+'.json',file_types=('Datos JSON (*.json)',))
                if not rutas:
                    return {'ok':True,'mensaje':'Exportación cancelada.'}
                Path(rutas[0]).write_text(json.dumps(self._hotel.datos,ensure_ascii=False,indent=2),encoding='utf-8')
                return {'ok':True,'mensaje':'Copia exportada correctamente.'}
            except OSError as error:
                return {'ok':False,'mensaje':str(error)}

    def importar(self, revision):
        import webview
        with self._lock:
            antes = deepcopy(self._hotel.datos)
            try:
                if type(revision) != int or revision != self._revision:
                    raise ValueError('Actualiza la vista antes de importar.')
                rutas = self._ventana.create_file_dialog(webview.FileDialog.OPEN,allow_multiple=False,file_types=('Datos JSON (*.json)',))
                if not rutas:
                    return {'ok':True,'mensaje':'Importación cancelada.','datos':self._estado()}
                datos = self._repo.leer(rutas[0])
                validar(datos)
                self._repo.guardar(datos)
                self._hotel = Hotel(datos,self._reloj)
                self._revision = self._revision+1
                return {'ok':True,'mensaje':'Copia importada. Se conservó el archivo anterior.','datos':self._estado()}
            except (ValueError,TypeError,KeyError,OSError) as error:
                self._hotel = Hotel(antes,self._reloj)
                return {'ok':False,'mensaje':str(error),'datos':self._estado()}
