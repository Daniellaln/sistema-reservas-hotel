import unittest
from copy import deepcopy
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from api import API
from repositorio import validar

class Limpieza(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(dir=Path(__file__).parent)
        self.hoy=[date(2026,10,13)]
        self.reloj=lambda:self.hoy[0]
        self.tiempo=[1000.0]
        self.segundos=lambda:self.tiempo[0]
        self.api=API(self.tmp.name,self.reloj,self.segundos)
        self.operar('huesped',{'dni':'12345678','nombre':'Daniella León'})
        self.operar('reserva',{'dni':'12345678','numero':'101','entrada':'2026-10-13','salida':'2026-10-14','personas':'1'})
        self.reserva=self.api.estado()['reservas'][0]['id']
    def tearDown(self):
        self.tmp.cleanup()
    def operar(self,accion,datos):
        return self.api.operar(accion,datos,self.api.estado()['revision'])
    def salir(self):
        self.assertTrue(self.operar('estado',{'id':self.reserva,'estado':'En estancia'})['ok'])
        self.assertTrue(self.operar('pago',{'id':self.reserva,'monto':'80','metodo':'Efectivo'})['ok'])
        self.hoy[0]=date(2026,10,14)
        self.assertTrue(self.operar('estado',{'id':self.reserva,'estado':'Finalizada'})['ok'])

    def test_checkout_reserva_y_limpieza_persisten(self):
        self.salir()
        resultado=self.operar('reserva',{'dni':'12345678','numero':'101','entrada':'2026-10-14','salida':'2026-10-15','personas':'1'})
        self.assertTrue(resultado['ok'])
        siguiente=resultado['datos']['reservas'][-1]['id']
        self.assertEqual(resultado['datos']['habitaciones'][0]['estado'],'Pendiente de limpieza')
        self.api=API(self.tmp.name,self.reloj,self.segundos)
        self.assertFalse(self.operar('estado',{'id':siguiente,'estado':'En estancia'})['ok'])
        self.assertEqual(self.api.estado()['reservas'][-1]['estado'],'Confirmada')
        self.assertTrue(self.operar('limpiar',{'numero':'101'})['ok'])
        self.assertEqual(self.api.estado()['habitaciones'][0]['estado'],'Limpiando')
        self.tiempo[0]+=5
        self.assertEqual(self.api.estado()['habitaciones'][0]['estado'],'Reservada')
        self.api=API(self.tmp.name,self.reloj,self.segundos)
        self.assertFalse(self.api.estado()['habitaciones'][0]['limpieza'])
        self.assertTrue(self.operar('estado',{'id':siguiente,'estado':'En estancia'})['ok'])

    def test_limpieza_no_habilita_mantenimiento(self):
        self.salir()
        self.assertTrue(self.operar('mantenimiento',{'numero':'101'})['ok'])
        self.assertFalse(self.operar('limpiar',{'numero':'101'})['ok'])
        self.assertTrue(self.api.estado()['habitaciones'][0]['limpieza'])
        self.assertFalse(self.operar('mantenimiento',{'numero':'101'})['ok'])
        self.tiempo[0]+=15
        self.assertEqual(self.api.estado()['habitaciones'][0]['estado'],'Pendiente de limpieza')
        self.assertTrue(self.operar('limpiar',{'numero':'101'})['ok'])
        self.assertFalse(self.operar('limpiar',{'numero':'101'})['ok'])

    def test_copia_antigua_y_estados_invalidos(self):
        datos=deepcopy(self.api._hotel.datos)
        for h in datos['habitaciones']:
            h.pop('limpieza')
        validar(datos)
        self.assertFalse(datos['habitaciones'][0]['limpieza'])
        datos['habitaciones'][0]['limpieza']='si'
        with self.assertRaises(ValueError):validar(datos)
        datos['habitaciones'][0]['limpieza']=True
        datos['reservas'][0]['estado']='En estancia'
        with self.assertRaises(ValueError):validar(datos)

    def test_checkout_con_deuda_no_marca_sucia(self):
        self.assertTrue(self.operar('estado',{'id':self.reserva,'estado':'En estancia'})['ok'])
        self.assertFalse(self.operar('estado',{'id':self.reserva,'estado':'Finalizada'})['ok'])
        habitacion=self.api.estado()['habitaciones'][0]
        self.assertEqual(habitacion['estado'],'Ocupada')
        self.assertFalse(habitacion['limpieza'])


    def test_cronometro_limpieza_y_reinicio(self):
        self.salir()
        r=self.operar('limpiar',{'numero':'101'})
        self.assertTrue(r['ok'])
        self.assertEqual(r['datos']['habitaciones'][0]['trabajo']['transcurrido'],0)
        self.assertFalse(self.operar('limpiar',{'numero':'101'})['ok'])
        self.assertFalse(self.operar('mantenimiento',{'numero':'101'})['ok'])
        self.tiempo[0]+=4.9
        self.api=API(self.tmp.name,self.reloj,self.segundos)
        h=self.api.estado()['habitaciones'][0]
        self.assertEqual(h['estado'],'Limpiando')
        self.assertEqual(h['trabajo']['transcurrido'],4)
        self.tiempo[0]+=.1
        self.assertEqual(self.api.estado()['habitaciones'][0]['estado'],'Disponible')
        historial=len(self.api.estado()['historial'])
        self.assertEqual(len(self.api.estado()['historial']),historial)

    def test_cronometro_mantenimiento_bloquea_reserva(self):
        r=self.operar('mantenimiento',{'numero':'102'})
        self.assertTrue(r['ok'])
        h=r['datos']['habitaciones'][1]
        self.assertEqual(h['estado'],'En mantenimiento')
        self.assertEqual(h['trabajo']['transcurrido'],0)
        self.assertFalse(self.operar('reserva',{'dni':'12345678','numero':'102','entrada':'2026-10-13','salida':'2026-10-14','personas':'1'})['ok'])
        self.tiempo[0]+=14
        self.assertEqual(self.api.estado()['habitaciones'][1]['trabajo']['transcurrido'],14)
        self.tiempo[0]+=1
        self.assertEqual(self.api.estado()['habitaciones'][1]['estado'],'Disponible')
        self.assertTrue(self.operar('reserva',{'dni':'12345678','numero':'102','entrada':'2026-10-13','salida':'2026-10-14','personas':'1'})['ok'])

    def test_cronometro_corrupto_y_error_de_guardado(self):
        from unittest.mock import patch
        self.salir()
        self.operar('limpiar',{'numero':'101'})
        datos=deepcopy(self.api._hotel.datos)
        datos['habitaciones'][0]['trabajo']['duracion']=0
        with self.assertRaises(ValueError):validar(datos)
        datos['habitaciones'][0]['trabajo']['duracion']=5
        datos['habitaciones'][0]['trabajo']['inicio']=float('nan')
        with self.assertRaises(ValueError):validar(datos)
        self.tiempo[0]+=5
        with patch.object(self.api._repo,'guardar',side_effect=OSError('disco')):
            with self.assertRaises(OSError):self.api.estado()
        self.assertTrue(self.api._hotel.datos['habitaciones'][0]['limpieza'])
        self.assertIsNotNone(self.api._hotel.datos['habitaciones'][0]['trabajo'])
        self.assertEqual(self.api.estado()['habitaciones'][0]['estado'],'Disponible')
