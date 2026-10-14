import unittest
from datetime import date
from modelo import Hotel

class Reservas(unittest.TestCase):
    def setUp(self):
        self.h = Hotel(reloj=lambda:date(2026,10,13))
        self.h.huesped('12345678','Daniella León')
        self.h.huesped('87654321','Daniella León')

    def crear(self):
        return self.h.reserva('12345678','101','2026-10-13','2026-10-15',1)

    def test_homonimos(self):
        self.assertEqual(self.h.indice.buscar('12345678')['dni'],'12345678')
        with self.assertRaises(ValueError):self.h.huesped('12345678','Otro')

    def test_fechas(self):
        for a,b in [('2020-01-01','2020-01-02'),('2026-10-13','2026-10-13'),('2027-02-30','2027-03-01'),('2026-10-15','2026-10-14')]:
            with self.assertRaises(ValueError):self.h.reserva('12345678','101',a,b,1)

    def test_fecha_basica_no_rompe_comparacion(self):
        with self.assertRaises(ValueError):
            self.h.reserva('12345678','101','20261013','20261015',1)

    def test_intervalos(self):
        r = self.crear()
        with self.assertRaises(ValueError):self.h.reserva('87654321','101','2026-10-14','2026-10-16',1)
        otro = self.h.reserva('87654321','101','2026-10-15','2026-10-16',1)
        self.assertNotEqual(r['id'],otro['id'])
        self.assertEqual(r['total'],16000)

    def test_capacidad(self):
        with self.assertRaises(ValueError):self.h.reserva('12345678','101','2026-10-13','2026-10-14',2)

    def test_cancelacion(self):
        r = self.crear()
        self.h.estado(r['id'],'Cancelada')
        self.assertTrue(self.h.disponible('101','2026-10-13','2026-10-15'))
        with self.assertRaises(ValueError):self.h.estado(r['id'],'En estancia')

    def test_checkin_futuro(self):
        r = self.h.reserva('12345678','101','2026-10-15','2026-10-16',1)
        with self.assertRaises(ValueError):self.h.estado(r['id'],'En estancia')

    def test_espera(self):
        self.crear()
        self.h.esperar('87654321','2026-10-13','2026-10-15',1)
        with self.assertRaises(ValueError):self.h.atender('101')
        self.assertEqual(len(self.h.cola.listar()),1)
        self.h.atender('102')
        self.assertEqual(len(self.h.cola.listar()),0)

    def test_mantenimiento(self):
        self.crear()
        with self.assertRaises(ValueError):self.h.mantenimiento('101')
        self.h.mantenimiento('201')
        self.assertFalse(self.h.disponible('201','2026-10-13','2026-10-15'))
