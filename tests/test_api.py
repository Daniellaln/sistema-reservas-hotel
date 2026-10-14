import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from datetime import date
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import json
import sys
from api import API

class Puente(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(dir=Path(__file__).parent)
        self.api=API(self.tmp.name,reloj=lambda:date(2026,10,13))
    def tearDown(self):self.tmp.cleanup()
    def ejecutar(self,accion,datos):
        return self.api.operar(accion,datos,self.api.estado()['revision'])
    def demo(self):
        self.assertTrue(self.ejecutar('demo',{})['ok'])

    def test_flujo(self):
        self.demo()
        r=self.api.estado()['reservas'][0]
        resultado=self.ejecutar('pago',{'id':r['id'],'monto':'10.25','metodo':'Yape'})
        self.assertTrue(resultado['ok'])
        self.assertEqual(resultado['datos']['reservas'][0]['saldo'],14975)
        self.assertTrue(self.ejecutar('estado',{'id':r['id'],'estado':'En estancia'})['ok'])
        self.assertFalse(self.ejecutar('estado',{'id':r['id'],'estado':'Finalizada'})['ok'])
        self.assertTrue(self.ejecutar('pago',{'id':r['id'],'monto':'149.75','metodo':'Efectivo'})['ok'])
        self.assertTrue(self.ejecutar('estado',{'id':r['id'],'estado':'Finalizada'})['ok'])
        nuevo=API(self.tmp.name)
        self.assertEqual(nuevo.estado()['reservas'][0]['estado'],'Finalizada')

    def test_doble_clic(self):
        self.demo();estado=self.api.estado();r=estado['reservas'][0]
        def cobrar():return self.api.operar('pago',{'id':r['id'],'monto':'1','metodo':'Yape'},estado['revision'])
        with ThreadPoolExecutor(max_workers=2) as pool:
            resultados=list(pool.map(lambda _:cobrar(),[1,2]))
        self.assertEqual(sum(x['ok'] for x in resultados),1)
        self.assertEqual(len(self.api.estado()['pagos']),1)

    def test_fallo_guardado_revierte_memoria(self):
        self.demo();antes=self.api.estado()
        with patch.object(self.api._repo,'guardar',side_effect=OSError('No se puede escribir')):
            resultado=self.ejecutar('huesped',{'dni':'10000003','nombre':'Nuevo','telefono':''})
        self.assertFalse(resultado['ok'])
        self.assertEqual(self.api.estado()['huespedes'],antes['huespedes'])

    def test_cotizacion_y_busqueda(self):
        self.demo()
        self.assertEqual(self.api.buscar('10000001')['nombre'],'Valeria Torres')
        self.assertIsNone(self.api.buscar('99999999'))
        q=self.api.cotizar('201','2026-10-13','2026-10-15','2')
        self.assertEqual(q['total'],32000)
        self.assertTrue(q['disponible'])
        self.assertFalse(self.api.cotizar('101','2026-10-13','2026-10-15','2')['ok'])

    def test_payloads(self):
        for accion,datos in [('reserva',{}),('huesped',{'dni':None}),('habitacion',{'capacidad':True}),('desconocida',{}),('reserva',{'personas':'1.5'})]:
            self.assertFalse(self.ejecutar(accion,datos)['ok'])

    def test_demo_no_sobrescribe(self):
        self.demo();self.assertFalse(self.ejecutar('demo',{})['ok'])

    def test_merge_sort_usado(self):
        self.demo()
        with patch('api.merge_sort',wraps=__import__('algoritmos').merge_sort) as m:
            d=self.api.estado('total')
            m.assert_called_once()
            self.assertLessEqual(d['reservas'][0]['total'],d['reservas'][1]['total'])

    def test_historial_recorre_en_python_y_conserva_sentido(self):
        self.demo()
        lista = self.api._hotel.historial
        with patch.object(lista,'listar',wraps=lista.listar) as recorrido:
            antiguos = self.api.estado('entrada',False)['historial']
            recorrido.assert_called_once_with(False)
        with patch.object(lista,'listar',wraps=lista.listar) as recorrido:
            recientes = self.api.estado('entrada',True)['historial']
            recorrido.assert_called_once_with(True)
        self.assertEqual(antiguos,list(reversed(recientes)))
        self.api.estado('entrada',False)
        resultado = self.api.operar('huesped',{'dni':'30000000','nombre':'Nuevo'},self.api._revision)
        self.assertTrue(resultado['ok'])
        self.assertEqual(resultado['datos']['historial'][-1]['accion'],'Huésped registrado · 30000000')

    def test_huespedes_se_listan_con_inorden_del_arbol(self):
        for dni in ['40000000','20000000','60000000']:
            self.assertTrue(self.ejecutar('huesped',{'dni':dni,'nombre':'Prueba'})['ok'])
        arbol = self.api._hotel.indice
        with patch.object(arbol,'listar',wraps=arbol.listar) as recorrido:
            datos = self.api.estado()
            recorrido.assert_called_once_with()
        self.assertEqual([h['dni'] for h in datos['huespedes']],['20000000','40000000','60000000'])

    def test_orden_invalido_no_cambia_preferencia(self):
        self.api.estado('total',False)
        for orden,inverso in [('otro',True),('entrada',1),('entrada','false')]:
            with self.assertRaises(ValueError):
                self.api.estado(orden,inverso)
        self.assertEqual(self.api._orden,'total')
        self.assertIs(self.api._inverso,False)

    def test_reportes(self):
        self.demo()
        r=self.api.estado()['reservas'][0]
        self.ejecutar('pago',{'id':r['id'],'monto':'10','metodo':'Yape'})
        reporte=self.api.reportes('2000-01-01','2099-12-31')
        self.assertEqual(reporte['ingresos'],1000)
        self.assertEqual(reporte['reservas'],2)
        self.assertEqual(reporte['noches'],5)
        self.assertFalse(self.api.reportes('2026-10-15','2026-10-14')['ok'])

    def test_orden_se_conserva_al_guardar(self):
        self.demo()
        self.api.estado('total')
        resultado=self.api.operar('huesped',{'dni':'10000003','nombre':'Otro','telefono':''},1)
        self.assertTrue(resultado['ok'])
        totales=[r['total'] for r in resultado['datos']['reservas']]
        self.assertEqual(totales,sorted(totales))

    def test_bloqueo_de_segunda_instancia(self):
        import sys
        if sys.platform != 'win32':
            self.skipTest('Bloqueo de Windows')
        from app import bloquear
        primero=bloquear(Path(self.tmp.name))
        try:
            with self.assertRaises(ValueError):bloquear(Path(self.tmp.name))
        finally:primero.close()
        segundo=bloquear(Path(self.tmp.name))
        segundo.close()

    def test_cancelada_no_se_suma_a_deuda(self):
        self.demo()
        r=self.api.estado()['reservas'][0]
        resultado=self.ejecutar('estado',{'id':r['id'],'estado':'Cancelada'})
        self.assertTrue(resultado['ok'])
        self.assertEqual(resultado['datos']['resumen']['pendiente'],39000)
        self.assertEqual(len(resultado['datos']['reservas']),2)

    def test_importacion_invalida_conserva_estado_y_archivo(self):
        self.demo()
        antes=self.api.estado()
        archivo=self.api._repo.archivo.read_text(encoding='utf-8')
        invalido=Path(self.tmp.name)/'invalido.json'
        invalido.write_text('{error',encoding='utf-8')
        self.api._ventana=SimpleNamespace(create_file_dialog=lambda *a,**k:[str(invalido)])
        modulo=SimpleNamespace(FileDialog=SimpleNamespace(OPEN=10))
        with patch.dict(sys.modules,{'webview':modulo}):
            resultado=self.api.importar(antes['revision'])
        self.assertFalse(resultado['ok'])
        self.assertEqual(self.api.estado(),antes)
        self.assertEqual(self.api._repo.archivo.read_text(encoding='utf-8'),archivo)

    def test_revision_booleana_no_importa(self):
        self.api._ventana=SimpleNamespace(create_file_dialog=lambda *a,**k:None)
        modulo=SimpleNamespace(FileDialog=SimpleNamespace(OPEN=10))
        with patch.dict(sys.modules,{'webview':modulo}):
            resultado=self.api.importar(False)
        self.assertFalse(resultado['ok'])

    def test_reserva_registra_huesped_en_un_paso(self):
        r=self.ejecutar('reserva',{'nuevo':'1','dni':'20000001','nombre':'Ana','telefono':'','numero':'101','entrada':'2026-10-13','salida':'2026-10-15','personas':'1'})
        self.assertTrue(r['ok'])
        self.assertEqual(len(r['datos']['huespedes']),1)
        self.assertEqual(len(r['datos']['reservas']),1)

    def test_reserva_fallida_no_deja_huesped_suelto(self):
        r=self.ejecutar('reserva',{'nuevo':'1','dni':'20000001','nombre':'Ana','telefono':'','numero':'101','entrada':'2026-10-13','salida':'2026-10-15','personas':'3'})
        self.assertFalse(r['ok'])
        self.assertEqual(r['datos']['huespedes'],[])

    def test_habitacion_reservada_hoy_no_se_ofrece_como_disponible(self):
        self.demo()
        habitaciones={h['numero']:h for h in self.api.estado()['habitaciones']}
        self.assertEqual(habitaciones['101']['estado'],'Reservada')
        self.assertEqual(habitaciones['102']['estado'],'Disponible')

    def test_reserva_futura_explica_bloqueo_de_mantenimiento(self):
        self.demo()
        habitaciones={h['numero']:h for h in self.api.estado()['habitaciones']}
        self.assertEqual(habitaciones['102']['estado'],'Disponible')
        self.assertEqual(habitaciones['102']['proxima_reserva'],'2026-10-14')
        self.assertFalse(habitaciones['102']['puede_mantenimiento'])
        self.assertTrue(habitaciones['201']['puede_mantenimiento'])
        self.assertFalse(self.ejecutar('mantenimiento',{'numero':'102'})['ok'])
