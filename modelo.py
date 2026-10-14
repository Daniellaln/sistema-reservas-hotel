"""Estructuras propias y reglas de recepción, sin dependencias externas."""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from uuid import uuid4
from estructuras import colaEnlazada, listaDoble, arbolBinario

class cuenta:
    def lon(self, pagos, identificador):
        total = 0
        for pago in pagos:
            if pago['reserva'] == identificador:
                total = total + pago['monto']
        return total


class calendario:
    def leona(self, entrada, salida, reserva):
        if entrada < reserva['salida'] and salida > reserva['entrada']:
            return True
        return False


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)

def centimos(texto):
    try:
        valor = Decimal(str(texto))
        exigir(valor.is_finite() and 0 < valor <= Decimal('1000000'), 'Monto fuera de rango.')
        exigir(valor * 100 == (valor * 100).to_integral_value(), 'Usa como máximo dos decimales.')
        return int(valor * 100)
    except InvalidOperation:
        raise ValueError('Monto inválido.')

class Hotel:

    def __init__(self, datos=None, reloj=date.today):
        self.reloj = reloj
        self.datos = datos if datos is not None else {'version': 1, 'huespedes': [], 'habitaciones': [{'numero': '101', 'tipo': 'Simple', 'capacidad': 1, 'tarifa': 8000, 'mantenimiento': False}, {'numero': '102', 'tipo': 'Doble', 'capacidad': 2, 'tarifa': 13000, 'mantenimiento': False}, {'numero': '201', 'tipo': 'Matrimonial', 'capacidad': 2, 'tarifa': 16000, 'mantenimiento': False}], 'reservas': [], 'pagos': [], 'espera': [], 'historial': []}
        self.indice = arbolBinario()
        for h in self.datos['huespedes']:
            self.indice.agregar(h['dni'], h)
        self.cola = colaEnlazada(self.datos['espera'])
        self.historial = listaDoble(self.datos['historial'])

    def registrar(self, texto):
        self.historial.agregar({'fecha': datetime.now().isoformat(timespec='seconds'), 'accion': texto})
        self.datos['historial'] = list(self.historial.listar())

    def huesped(self, dni, nombre, telefono=''):
        exigir(len(dni) == 8 and dni.isascii() and dni.isdigit(), 'El DNI debe tener 8 dígitos.')
        exigir(2 <= len(nombre.strip()) <= 100, 'Nombre de 2 a 100 caracteres.')
        exigir(not self.indice.buscar(dni), 'Ese DNI ya existe.')
        exigir(len(telefono) <= 30, 'Teléfono demasiado largo.')
        h = {'dni': dni, 'nombre': nombre.strip(), 'telefono': telefono.strip()}
        self.datos['huespedes'].append(h)
        self.indice.agregar(dni, h)
        self.registrar('Huésped registrado · ' + dni)

    def habitacion(self, numero, tipo, capacidad, tarifa):
        exigir(numero.isascii() and numero.isdigit() and (1 <= len(numero) <= 4), 'Número inválido.')
        exigir(self.buscar_habitacion(numero) == None, 'Número ya registrado.')
        exigir(tipo in ['Simple', 'Doble', 'Matrimonial', 'Suite'], 'Tipo inválido.')
        exigir(1 <= capacidad <= 20, 'Capacidad de 1 a 20 personas.')
        self.datos['habitaciones'].append({'numero': numero, 'tipo': tipo, 'capacidad': capacidad, 'tarifa': centimos(tarifa), 'mantenimiento': False})
        self.registrar('Habitación registrada · ' + numero)

    def rango(self, entrada, salida):
        try:
            a, b = (date.fromisoformat(entrada), date.fromisoformat(salida))
        except (ValueError, TypeError):
            raise ValueError('Fecha inválida.')
        exigir(a >= self.reloj(), 'No puedes reservar una entrada en el pasado.')
        exigir(1 <= (b - a).days <= 365, 'La estadía debe durar entre 1 y 365 noches.')
        return (b - a).days

    def buscar_habitacion(self, numero):
        for habitacion in self.datos['habitaciones']:
            if habitacion['numero'] == numero:
                return habitacion
        return None

    def tiene_reservas(self, numero):
        for reserva in self.datos['reservas']:
            if reserva['habitacion'] == numero:
                if reserva['estado'] in ['Confirmada', 'En estancia']:
                    return True
        return False

    def tiene_estancia(self, numero):
        for reserva in self.datos['reservas']:
            if reserva['habitacion'] == numero and reserva['estado'] == 'En estancia':
                return True
        return False

    def disponible(self, numero, entrada, salida):
        habitacion = self.buscar_habitacion(numero)
        if habitacion == None:
            return False
        if habitacion['mantenimiento'] == True:
            return False
        for reserva in self.datos['reservas']:
            if reserva['habitacion'] == numero:
                if reserva['estado'] in ['Confirmada', 'En estancia']:
                    soy = calendario()
                    if soy.leona(entrada, salida, reserva):
                        return False
        return True

    def reserva(self, dni, numero, entrada, salida, personas):
        exigir(self.indice.buscar(dni), 'Selecciona un huésped registrado.')
        noches = self.rango(entrada, salida)
        h = self.buscar_habitacion(numero)
        exigir(h, 'Habitación inexistente.')
        exigir(1 <= personas <= h['capacidad'], 'La cantidad excede la capacidad de la habitación.')
        exigir(self.disponible(numero, entrada, salida), 'La habitación no está disponible para esas fechas.')
        r = {'id': str(uuid4()), 'dni': dni, 'habitacion': numero, 'entrada': entrada, 'salida': salida, 'personas': personas, 'total': noches * h['tarifa'], 'estado': 'Confirmada'}
        self.datos['reservas'].append(r)
        self.registrar('Reserva confirmada · ' + r['id'][:8])
        return r

    def obtener(self, identificador):
        r = None
        for reserva in self.datos['reservas']:
            if reserva['id'] == identificador:
                r = reserva
                break
        exigir(r, 'Reserva inexistente.')
        return r

    def saldo(self, identificador):
        reserva = self.obtener(identificador)
        chu = cuenta()
        pagado = chu.lon(self.datos['pagos'], identificador)
        pendiente = reserva['total'] - pagado
        return pendiente

    def pago(self, identificador, monto, metodo):
        r = self.obtener(identificador)
        exigir(r['estado'] in ['Confirmada', 'En estancia'], 'Esta reserva no admite pagos.')
        n = centimos(monto)
        exigir(n <= self.saldo(identificador), 'El pago supera el saldo pendiente.')
        exigir(metodo in ['Efectivo', 'Tarjeta', 'Yape', 'Transferencia'], 'Método inválido.')
        self.datos['pagos'].append({'id': str(uuid4()), 'reserva': identificador, 'monto': n, 'metodo': metodo, 'fecha': datetime.now().isoformat(timespec='seconds')})
        self.registrar('Cobro ' + metodo + ' · ' + identificador[:8])

    def estado(self, identificador, estado):
        r = self.obtener(identificador)
        if estado == 'Cancelada':
            exigir(r['estado'] == 'Confirmada', 'Solo se cancelan reservas confirmadas.')
            exigir(self.saldo(identificador) == r['total'], 'Tiene pagos. Esta versión no procesa reembolsos.')
        elif estado == 'En estancia':
            exigir(r['estado'] == 'Confirmada', 'La reserva no está confirmada.')
            exigir(r['entrada'] <= self.reloj().isoformat() < r['salida'], 'El check-in debe estar dentro de las fechas reservadas.')
            exigir(not self.tiene_estancia(r['habitacion']), 'Hay una estancia abierta; realiza su check-out.')
        elif estado == 'Finalizada':
            exigir(r['estado'] == 'En estancia', 'Primero realiza el check-in.')
            exigir(self.saldo(identificador) == 0, 'Cobra el saldo antes del check-out.')
        else:
            raise ValueError('Estado inválido.')
        r['estado'] = estado
        self.registrar(estado + ' · ' + identificador[:8])

    def mantenimiento(self, numero):
        h = self.buscar_habitacion(numero)
        exigir(h, 'Habitación inexistente.')
        if not h['mantenimiento']:
            exigir(not self.tiene_reservas(numero), 'Tiene reservas vigentes: no puede entrar en mantenimiento.')
        h['mantenimiento'] = not h['mantenimiento']
        self.registrar('Mantenimiento actualizado · ' + numero)

    def esperar(self, dni, entrada, salida, personas):
        exigir(self.indice.buscar(dni), 'Selecciona un huésped.')
        self.rango(entrada, salida)
        exigir(1 <= personas <= 20, 'Cantidad inválida.')
        exigir(not any((s['dni'] == dni and s['entrada'] == entrada and (s['salida'] == salida) for s in self.cola.listar())), 'La solicitud ya está en espera.')
        self.cola.encolar({'dni': dni, 'entrada': entrada, 'salida': salida, 'personas': personas})
        self.datos['espera'] = list(self.cola.listar())
        self.registrar('Solicitud en espera · ' + dni)

    def atender(self, numero):
        exigir(self.cola.Ini, 'La cola está vacía.')
        s = self.cola.Ini.dato
        r = self.reserva(s['dni'], numero, s['entrada'], s['salida'], s['personas'])
        self.cola.desencolar()
        self.datos['espera'] = list(self.cola.listar())
        return r

    def retirar_espera(self):
        exigir(self.cola.Ini, 'La cola está vacía.')
        self.cola.desencolar()
        self.datos['espera'] = list(self.cola.listar())
        self.registrar('Primera solicitud retirada de espera')
