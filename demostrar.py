"""Ejecutar con Python: usa las mismas clases y el puente de la aplicación."""
from datetime import date, timedelta
from tempfile import TemporaryDirectory
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / "proyecto"))
from api import API


def ejecutar(api, accion, datos):
    resultado = api.operar(accion, datos, api._revision)
    if resultado['ok'] == False:
        raise ValueError(resultado['mensaje'])
    return resultado['datos']


def demostrar():
    with TemporaryDirectory(prefix='hotel-demostracion-') as carpeta:
        hoy = date.today()
        entrada = hoy.isoformat()
        salida = (hoy + timedelta(days=1)).isoformat()
        api = API(carpeta, reloj=lambda: hoy, segundos=lambda: 100.0)
        hotel = api._hotel

        print('\n1. ÁRBOL BINARIO: insertar, buscar y recorrer inorden')
        for dni, nombre in [('40000000','Daniella'),('20000000','Ana'),('60000000','Luis')]:
            ejecutar(api,'huesped',{'dni':dni,'nombre':nombre})
        tmp = hotel.indice.Raiz
        print('Raíz:',tmp.clave,'| Izquierda:',tmp.izq.clave,'| Derecha:',tmp.der.clave)
        print('Búsqueda real por el puente:',api.buscar('20000000'))
        print('Inorden que recibe la interfaz:')
        for h in api.estado()['huespedes']:
            print(h['dni'],h['nombre'])

        print('\n2. RESERVAS: disponibilidad y detección de solapamiento')
        for dni, numero in [('40000000','201'),('20000000','101'),('60000000','102')]:
            ejecutar(api,'reserva',{'dni':dni,'numero':numero,'entrada':entrada,'salida':salida,'personas':'1'})
        resultado = api.operar('reserva',{'dni':'60000000','numero':'101','entrada':entrada,'salida':salida,'personas':'1'},api._revision)
        assert resultado['ok'] == False
        print('Cruce rechazado:',resultado['mensaje'])
        hotel = api._hotel

        print('\n3. MERGE SORT: misma API que ordena la agenda')
        for r in api.estado('total')['reservas']:
            print('Habitación',r['habitacion'],'| Total en centavos:',r['total'])

        print('\n4. COLA ENLAZADA: primero en entrar, primero en salir')
        for dni in ['40000000','60000000']:
            ejecutar(api,'espera',{'dni':dni,'entrada':entrada,'salida':salida,'personas':'1'})
        primero = hotel.cola.Ini
        print('Inicio:',primero.dato['dni'],'-> siguiente:',primero.der.dato['dni'])
        resultado = api.operar('atender',{'numero':'101'},api._revision)
        assert resultado['ok'] == False
        hotel = api._hotel
        assert hotel.cola.Ini.dato['dni'] == '40000000'
        print('Sin habitación disponible, la primera solicitud se conserva.')
        reserva = None
        for r in hotel.datos['reservas']:
            if r['habitacion'] == '101':
                reserva = r
        ejecutar(api,'estado',{'id':reserva['id'],'estado':'Cancelada'})
        ejecutar(api,'atender',{'numero':'101'})
        print('Atendida: 40000000 | Nuevo inicio:',hotel.cola.Ini.dato['dni'])

        print('\n5. COBROS: recorrido y acumulador; check-in y checkout')
        for r in hotel.datos['reservas']:
            if r['habitacion'] == '101' and r['estado'] == 'Confirmada':
                reserva = r
        ejecutar(api,'estado',{'id':reserva['id'],'estado':'En estancia'})
        ejecutar(api,'pago',{'id':reserva['id'],'monto':'30','metodo':'Yape'})
        print('Saldo tras abonar S/30:',hotel.saldo(reserva['id']),'centavos')
        resultado = api.operar('pago',{'id':reserva['id'],'monto':'51','metodo':'Yape'},api._revision)
        assert resultado['ok'] == False
        print('Sobrepago rechazado:',resultado['mensaje'])
        hotel = api._hotel
        ejecutar(api,'pago',{'id':reserva['id'],'monto':'50','metodo':'Efectivo'})
        ejecutar(api,'estado',{'id':reserva['id'],'estado':'Finalizada'})

        print('\n6. LIMPIEZA: Python compara el plazo almacenado')
        ejecutar(api,'limpiar',{'numero':'101'})
        api._segundos = lambda: 104.0
        api.estado()
        assert hotel.buscar_habitacion('101')['limpieza'] == True
        api._segundos = lambda: 105.0
        api.estado()
        assert hotel.buscar_habitacion('101')['limpieza'] == False
        print('A los 4 segundos sigue limpiando; a los 5 termina.')
        print('El reloj se controla para demostrarlo sin esperar; la app usa tiempo real.')

        print('\n7. LISTA DOBLE: enlaces y recorridos desde Python')
        tmp = hotel.historial.Fin
        print('Último:',tmp.dato['accion'])
        print('Anterior por izq:',tmp.izq.dato['accion'])
        assert tmp.izq.der is tmp
        antiguos = api.estado('entrada',False)['historial']
        recientes = api.estado('entrada',True)['historial']
        assert antiguos == list(reversed(recientes))
        print('Desde Ini por der:',antiguos[0]['accion'])
        print('Desde Fin por izq:',recientes[0]['accion'])

        print('\n8. REPORTES Y DISCO: acumulación y recuperación de JSON')
        print(api.reportes(entrada,salida))
        nuevo = API(carpeta)
        assert nuevo.buscar('40000000')['nombre'] == 'Daniella'
        assert nuevo._hotel.saldo(reserva['id']) == 0
        print('Nueva instancia recupera huéspedes, reservas, pagos y estructuras.')
        print('\nDemostración terminada. Se usaron datos temporales, separados de recepción.')


if __name__ == '__main__':
    demostrar()
