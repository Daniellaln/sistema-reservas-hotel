"""Nodos y estructuras escritos paso a paso, como en los laboratorios."""

class nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None

    def __repr__(self):
        return str(self.dato)


class colaEnlazada:
    def __init__(self, datos=()):
        self.Ini = None
        self.Fin = None
        for dato in datos:
            self.encolar(dato)

    def encolar(self, dato):
        nuevo = nodo(dato)
        if self.Ini == None:
            self.Ini = nuevo
            self.Fin = nuevo
        else:
            self.Fin.der = nuevo
            self.Fin = nuevo

    def desencolar(self):
        if self.Ini == None:
            return None
        dato = self.Ini.dato
        self.Ini = self.Ini.der
        if self.Ini == None:
            self.Fin = None
        return dato

    def listar(self):
        L = []
        tmp = self.Ini
        while tmp != None:
            L.append(tmp.dato)
            tmp = tmp.der
        return L


class nodoArbol:
    def __init__(self, clave, dato):
        self.clave = clave
        self.dato = dato
        self.izq = None
        self.der = None


class arbolBinario:
    def __init__(self):
        self.Raiz = None

    def agregar(self, clave, dato):
        nuevo = nodoArbol(clave, dato)
        if self.Raiz == None:
            self.Raiz = nuevo
            return
        tmp = self.Raiz
        while tmp != None:
            if clave == tmp.clave:
                tmp.dato = dato
                return
            if clave < tmp.clave:
                if tmp.izq == None:
                    tmp.izq = nuevo
                    return
                tmp = tmp.izq
            else:
                if tmp.der == None:
                    tmp.der = nuevo
                    return
                tmp = tmp.der

    def buscar(self, clave):
        tmp = self.Raiz
        while tmp != None:
            if clave == tmp.clave:
                return tmp.dato
            if clave < tmp.clave:
                tmp = tmp.izq
            else:
                tmp = tmp.der
        return None

    def listar(self):
        L = []
        pendientes = []
        tmp = self.Raiz
        while tmp != None or len(pendientes) > 0:
            if tmp != None:
                pendientes.append(tmp)
                tmp = tmp.izq
            else:
                tmp = pendientes.pop()
                L.append(tmp.dato)
                tmp = tmp.der
        return L


class listaDoble:
    def __init__(self, datos=()):
        self.Ini = None
        self.Fin = None
        for dato in datos:
            self.agregar(dato)

    def agregar(self, dato):
        nuevo = nodo(dato)
        if self.Ini == None:
            self.Ini = nuevo
            self.Fin = nuevo
        else:
            nuevo.izq = self.Fin
            self.Fin.der = nuevo
            self.Fin = nuevo

    def listar(self, inverso=False):
        L = []
        if inverso == True:
            tmp = self.Fin
        else:
            tmp = self.Ini
        while tmp != None:
            L.append(tmp.dato)
            if inverso == True:
                tmp = tmp.izq
            else:
                tmp = tmp.der
        return L


