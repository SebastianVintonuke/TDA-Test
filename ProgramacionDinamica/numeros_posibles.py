


# Ecuación de recurrencia:
#
#             OPT(k, 0) = 0
#             OPT(k, 1) = 1
#
#             OPT(k, n) = sum_{j}( (OPT(j, n-1) ) ; siendo j cada número alcanzable desde k
#
# Complejidad: O(n) dado principalmente por recorrer las n longitudes

NUMEROS_ALCANZABLES_DESDE = {
    0: [8],
    1: [2,4],
    2: [3,5,1],
    3: [6,2],
    4: [1,5,7],
    5: [2,6,8,4],
    6: [9,5,3],
    7: [4,8],
    8: [5,9,0,7],
    9: [8,6],
}

def numeros_posibles(k, n):
    optimos = c_optimos(n)
    return optimos[k][n]

def c_optimos(n):
    optimos = [ [ 0 for _ in range(n+1) ] for _ in range(9+1) ] # 0(n)

    for numero in range(9+1): # 0(1)
        optimos[numero][0] = 0
        if n >= 1:
            optimos[numero][1] = 1

    for longitud in range(2, n+1): # 0(n)
        for numero in range(9+1): # 0(1)
            optimos[numero][longitud] = sum([ optimos[numero_alcanzable][longitud-1] for numero_alcanzable in NUMEROS_ALCANZABLES_DESDE[numero] ])

    return optimos















import unittest



class TestTecladoNumerico(unittest.TestCase):

    def test_longitud_uno(self):
        # Para N=1, siempre hay 1 posibilidad (el dígito mismo)
        for i in range(10):
            self.assertEqual(numeros_posibles(i, 1), 1)

    def test_longitud_dos(self):
        # Basado en los ejemplos de la consigna
        self.assertEqual(numeros_posibles(0, 2), 1)  # 0-8
        self.assertEqual(numeros_posibles(1, 2), 2)  # 1-2, 1-4
        self.assertEqual(numeros_posibles(2, 2), 3)  # 2-1, 2-3, 2-5
        self.assertEqual(numeros_posibles(5, 2), 4)  # 5-2, 5-4, 5-6, 5-8
        self.assertEqual(numeros_posibles(8, 2), 4)  # 8-0, 8-5, 8-7, 8-9

    def test_longitud_tres(self):
        # Ejemplo: Empezando en 0 longitud 3
        # 0 -> 8 -> [0, 5, 7, 9] (Total: 4 posibilidades: 080, 085, 087, 089)
        self.assertEqual(numeros_posibles(0, 3), 4)

        # Ejemplo: Empezando en 1 longitud 3
        # 1 -> 2 -> [1, 3, 5]
        # 1 -> 4 -> [1, 5, 7]
        # Total: 6 posibilidades
        self.assertEqual(numeros_posibles(1, 3), 6)

    def test_caso_n_cero(self):
        self.assertEqual(numeros_posibles(5, 0), 0)


if __name__ == '__main__':
    unittest.main()