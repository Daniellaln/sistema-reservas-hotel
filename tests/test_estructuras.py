import unittest
from estructuras import colaEnlazada, listaDoble, arbolBinario

class Estructuras(unittest.TestCase):
    def test_cola(self):
        c = colaEnlazada([10,20])
        self.assertEqual(c.desencolar(),10)
        self.assertEqual(c.desencolar(),20)
        self.assertIsNone(c.desencolar())
        self.assertIsNone(c.Fin)
        c.encolar(30)
        self.assertEqual(c.listar(),[30])

    def test_doble(self):
        L = listaDoble([10,20,30])
        self.assertEqual(L.listar(),[10,20,30])
        self.assertEqual(L.listar(True),[30,20,10])
        self.assertIs(L.Ini.der.izq,L.Ini)
        self.assertIsNone(L.Ini.izq)
        self.assertIsNone(L.Fin.der)

    def test_arbol(self):
        A = arbolBinario()
        for k in [5,3,7,2,4,6,8]:
            A.agregar(k,k)
        self.assertEqual(A.listar(),[2,3,4,5,6,7,8])
        self.assertEqual(A.buscar(6),6)
        self.assertIsNone(A.buscar(9))
        A.agregar(6,'nuevo')
        self.assertEqual(A.buscar(6),'nuevo')

    def test_arbol_desbalanceado(self):
        A = arbolBinario()
        for k in range(1100):
            A.agregar(k,k)
        self.assertEqual(A.buscar(1099),1099)
        self.assertEqual(len(A.listar()),1100)

if __name__ == '__main__':
    unittest.main()
