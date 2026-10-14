import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modelo import Hotel, centimos
from repositorio import Repositorio, validar

class Cobros(unittest.TestCase):
    def setUp(self):
        self.h=Hotel(reloj=lambda:date(2026,10,13))
        self.h.huesped('12345678','Daniella León')
        self.r=self.h.reserva('12345678','101','2026-10-13','2026-10-15',1)

    def test_parcial(self):
        self.h.pago(self.r['id'],'10.25','Yape')
        self.assertEqual(self.h.saldo(self.r['id']),14975)
        with self.assertRaises(ValueError):self.h.pago(self.r['id'],'150','Efectivo')
        with self.assertRaises(ValueError):self.h.estado(self.r['id'],'Cancelada')

    def test_checkout(self):
        self.h.estado(self.r['id'],'En estancia')
        with self.assertRaises(ValueError):self.h.estado(self.r['id'],'Finalizada')
        self.h.pago(self.r['id'],'160','Tarjeta')
        self.h.estado(self.r['id'],'Finalizada')
        with self.assertRaises(ValueError):self.h.pago(self.r['id'],'1','Yape')

    def test_decimal(self):
        self.assertEqual(centimos('0.10'),10)
        for valor in ['NaN','Infinity','0','-1','1.001']:
            with self.assertRaises(ValueError):centimos(valor)

    def test_archivo(self):
        with TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            repo=Repositorio(carpeta)
            repo.guardar(self.h.datos)
            self.h.pago(self.r['id'],'10','Yape')
            repo.guardar(self.h.datos)
            nuevo=Hotel(repo.leer())
            self.assertEqual(nuevo.saldo(self.r['id']),15000)
            self.assertTrue((Path(carpeta)/'hotel.anterior.json').exists())

    def test_archivo_danado_no_se_sobrescribe(self):
        with TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            repo=Repositorio(carpeta)
            repo.archivo.write_text('{error',encoding='utf-8')
            with self.assertRaises(ValueError):repo.leer()
            self.assertEqual(repo.archivo.read_text(encoding='utf-8'),'{error')

    def test_fallo_escritura_conserva_archivo(self):
        with TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            repo=Repositorio(carpeta);repo.guardar(self.h.datos)
            antes=repo.archivo.read_text(encoding='utf-8')
            self.h.pago(self.r['id'],'10','Yape')
            with patch('repositorio.os.replace',side_effect=OSError('Disco lleno')):
                with self.assertRaises(OSError):repo.guardar(self.h.datos)
            self.assertEqual(repo.archivo.read_text(encoding='utf-8'),antes)

    def test_importacion_sobrepago(self):
        self.h.pago(self.r['id'],'160','Yape')
        self.h.datos['pagos'][0]['monto']=16001
        with self.assertRaises(ValueError):validar(self.h.datos)

    def test_importacion_fechas_no_canonicas(self):
        self.r['entrada']='20261013'
        with self.assertRaises(ValueError):validar(self.h.datos)

    def test_version_booleana_rechazada(self):
        self.h.datos['version']=True
        with self.assertRaises(ValueError):validar(self.h.datos)

    def test_espera_importada_mayor_a_un_ano(self):
        self.h.datos['espera'].append({'dni':'12345678','entrada':'2026-10-13','salida':'2028-10-13','personas':1})
        with self.assertRaises(ValueError):validar(self.h.datos)
