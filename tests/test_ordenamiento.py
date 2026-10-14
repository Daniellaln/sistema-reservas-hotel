import unittest
import random
from algoritmos import merge_sort

class Ordenamiento(unittest.TestCase):
    def test_vacio(self):
        self.assertEqual(merge_sort([],'entrada'),[])

    def test_estable_y_no_modifica(self):
        L=[{'entrada':'2026-11-02','id':'A'},{'entrada':'2026-11-01','id':'B'},{'entrada':'2026-11-02','id':'C'}]
        ordenado=merge_sort(L,'entrada')
        self.assertEqual([x['id'] for x in ordenado],['B','A','C'])
        self.assertEqual(L[0]['id'],'A')

    def test_aleatorio(self):
        random.seed(7)
        L=[]
        for i in range(500):L.append({'total':random.randrange(1000),'id':i})
        self.assertEqual(merge_sort(L,'total'),sorted(L,key=lambda x:x['total']))
