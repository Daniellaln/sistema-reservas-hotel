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
        self.api=API(self.tmp.name,self.reloj)
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
        self.api=API(self.tmp.name,self.reloj)
        self.assertFalse(self.operar('estado',{'id':siguiente,'estado':'En estancia'})['ok'])
        self.assertEqual(self.api.estado()['reservas'][-1]['estado'],'Confirmada')
        self.assertTrue(self.operar('limpiar',{'numero':'101'})['ok'])
        self.assertEqual(self.api.estado()['habitaciones'][0]['estado'],'Reservada')
        self.api=API(self.tmp.name,self.reloj)
        self.assertFalse(self.api.estado()['habitaciones'][0]['limpieza'])
        self.assertTrue(self.operar('estado',{'id':siguiente,'estado':'En estancia'})['ok'])

    def test_limpieza_no_habilita_mantenimiento(self):
        self.salir()
        self.assertTrue(self.operar('mantenimiento',{'numero':'101'})['ok'])
        self.assertFalse(self.operar('limpiar',{'numero':'101'})['ok'])
        self.assertTrue(self.api.estado()['habitaciones'][0]['limpieza'])
        self.assertTrue(self.operar('mantenimiento',{'numero':'101'})['ok'])
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
