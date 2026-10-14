"""Lectura, validación y escritura atómica del archivo del hotel."""
import json
import os
import shutil
from math import isfinite
from pathlib import Path
from datetime import date, datetime
from uuid import UUID
from modelo import Hotel

def validar(datos):
    if not isinstance(datos, dict) or type(datos.get('version')) != int or datos.get('version') != 1:
        raise ValueError('Formato de datos no compatible.')
    for clave in ['huespedes','habitaciones','reservas','pagos','espera','historial']:
        if not isinstance(datos.get(clave),list) or len(datos[clave]) > 20000:
            raise ValueError('Colección inválida: '+clave)
    for coleccion, clave in [('huespedes','dni'),('habitaciones','numero'),('reservas','id'),('pagos','id')]:
        encontrados = set()
        for dato in datos[coleccion]:
            valor = dato[clave]
            if valor in encontrados:
                raise ValueError('Identificador duplicado.')
            encontrados.add(valor)
    for h in datos['huespedes']:
        if not isinstance(h['dni'],str) or not h['dni'].isascii() or not h['dni'].isdigit() or len(h['dni']) != 8:
            raise ValueError('DNI inválido.')
        if not isinstance(h['nombre'],str) or not 2 <= len(h['nombre'].strip()) <= 100 or not isinstance(h['telefono'],str) or len(h['telefono']) > 30:
            raise ValueError('Datos de huésped inválidos.')
    for h in datos['habitaciones']:
        if type(h.get('limpieza',False)) != bool:
            raise ValueError('Estado de limpieza inválido.')
        trabajo = h.get('trabajo')
        if trabajo != None:
            if not isinstance(trabajo,dict) or trabajo.get('tipo') not in ['Limpieza','Mantenimiento']:
                raise ValueError('Trabajo inválido.')
            duracion = 5 if trabajo['tipo'] == 'Limpieza' else 15
            inicio = trabajo.get('inicio')
            if type(inicio) not in [int,float] or not isfinite(inicio) or inicio < 0 or type(trabajo.get('duracion')) != int or trabajo['duracion'] != duracion:
                raise ValueError('Cronómetro inválido.')
            if trabajo['tipo'] == 'Limpieza' and (not h.get('limpieza',False) or h['mantenimiento']):
                raise ValueError('Limpieza en curso incompatible con la habitación.')
            if trabajo['tipo'] == 'Mantenimiento' and not h['mantenimiento']:
                raise ValueError('Mantenimiento en curso incompatible con la habitación.')
        if not isinstance(h['numero'],str) or not h['numero'].isascii() or not h['numero'].isdigit() or not 1 <= len(h['numero']) <= 4:
            raise ValueError('Número de habitación inválido.')
        if h['tipo'] not in ['Simple','Doble','Matrimonial','Suite'] or type(h['capacidad']) != int or not 1 <= h['capacidad'] <= 20 or type(h['tarifa']) != int or not 1 <= h['tarifa'] <= 100000000 or type(h['mantenimiento']) != bool:
            raise ValueError('Habitación inválida.')
    hotel = Hotel(datos)
    for r in datos['reservas']:
        UUID(r['id'])
        a = date.fromisoformat(r['entrada'])
        b = date.fromisoformat(r['salida'])
        if a.isoformat() != r['entrada'] or b.isoformat() != r['salida']:
            raise ValueError('Las fechas deben usar el formato AAAA-MM-DD.')
        h = hotel.buscar_habitacion(r['habitacion'])
        if not hotel.indice.buscar(r['dni']) or h == None or not 1 <= (b-a).days <= 365:
            raise ValueError('Referencias o fechas de reserva inválidas.')
        if type(r['personas']) != int or not 1 <= r['personas'] <= h['capacidad'] or type(r['total']) != int or not 1 <= r['total'] <= 36500000000 or r['estado'] not in ['Confirmada','En estancia','Finalizada','Cancelada']:
            raise ValueError('Reserva inválida.')
        if r['estado'] in ['Confirmada','En estancia']:
            if r['estado'] == 'En estancia' and h['limpieza']:
                raise ValueError('Una habitación pendiente de limpieza no puede tener una estancia abierta.')
            if h['mantenimiento']:
                raise ValueError('Hay reservas en una habitación en mantenimiento.')
            for otra in datos['reservas']:
                if otra['id'] != r['id'] and otra['habitacion'] == r['habitacion'] and otra['estado'] in ['Confirmada','En estancia']:
                    if r['entrada'] < otra['salida'] and r['salida'] > otra['entrada']:
                        raise ValueError('Hay reservas solapadas.')
                    if r['estado'] == 'En estancia' and otra['estado'] == 'En estancia':
                        raise ValueError('Dos estancias abiertas en la misma habitación.')
    for p in datos['pagos']:
        UUID(p['id'])
        hotel.obtener(p['reserva'])
        datetime.fromisoformat(p['fecha'])
        if type(p['monto']) != int or p['monto'] <= 0 or p['metodo'] not in ['Efectivo','Tarjeta','Yape','Transferencia']:
            raise ValueError('Pago inválido.')
    for r in datos['reservas']:
        saldo = hotel.saldo(r['id'])
        if saldo < 0 or (r['estado'] == 'Finalizada' and saldo != 0) or (r['estado'] == 'Cancelada' and saldo != r['total']):
            raise ValueError('Saldo incompatible con el estado de la reserva.')
    for s in datos['espera']:
        a = date.fromisoformat(s['entrada'])
        b = date.fromisoformat(s['salida'])
        if a.isoformat() != s['entrada'] or b.isoformat() != s['salida'] or not 1 <= (b-a).days <= 365:
            raise ValueError('Fechas de espera inválidas.')
        if not hotel.indice.buscar(s['dni']) or date.fromisoformat(s['salida']) <= date.fromisoformat(s['entrada']) or type(s['personas']) != int or not 1 <= s['personas'] <= 20:
            raise ValueError('Solicitud de espera inválida.')
    for item in datos['historial']:
        datetime.fromisoformat(item['fecha'])
        if not isinstance(item['accion'],str) or len(item['accion']) > 500:
            raise ValueError('Historial inválido.')

class Repositorio:
    def __init__(self, carpeta):
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True,exist_ok=True)
        self.archivo = self.carpeta / 'hotel.json'

    def leer(self, archivo=None):
        ruta = Path(archivo) if archivo else self.archivo
        if not ruta.exists():
            if archivo:
                raise ValueError('No se encontró el archivo elegido.')
            return Hotel().datos
        if ruta.stat().st_size > 10000000:
            raise ValueError('El archivo supera el máximo de 10 MB.')
        try:
            datos = json.loads(ruta.read_text(encoding='utf-8'))
            validar(datos)
            return datos
        except (ValueError,TypeError,KeyError,AttributeError) as error:
            raise ValueError('No se puede leer el archivo. Se ha conservado sin cambios. '+str(error))

    def guardar(self, datos):
        validar(datos)
        texto = json.dumps(datos,ensure_ascii=False,indent=2)
        if len(texto.encode('utf-8')) > 10000000:
            raise ValueError('Los datos superan el límite de 10 MB. Exporta una copia y revisa el historial.')
        temporal = self.carpeta / 'hotel.tmp'
        with temporal.open('w',encoding='utf-8') as archivo:
            archivo.write(texto)
            archivo.flush()
            os.fsync(archivo.fileno())
        if self.archivo.exists():
            shutil.copy2(self.archivo,self.carpeta / 'hotel.anterior.json')
        os.replace(temporal,self.archivo)
