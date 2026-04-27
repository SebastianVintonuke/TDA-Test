# Complejidad:
#
#        O(P * W) = O(P * 2^m)
#
# Ecuación de recurrencia:
#
#  OPT(i, w) =   si: (w-P[i] >= 0)   max(OPT(i-1, w-P[i])+P[i], OPT(i-1,w))
#                si no:              OPT(i-1,w)
#
# Es decir el maximo entre la familia i más el óptimo de la mesa sin el espacio que ocupa la familia i (siempre que el espacio sea mayor a cero) y el óptimo sin la familia i
def bodegon_dinamico(P, W):
    if not P or not W:
        return []
    optimos = c_optimos(P, W)
    return c_solucion(P, W, optimos)

def c_optimos(P, W):
    optimos = [ [ 0 for _ in range(W + 1) ] for _ in range(len(P) + 1) ]
    for i in range(1, len(P) + 1):
        for w in range(1, W + 1):
            espacio_restante = w - P[i-1]
            if espacio_restante >= 0:
                no_usar = optimos[i - 1][w]
                usar = optimos[i - 1][espacio_restante] + P[i-1]
                optimos[i][w] = max(no_usar, usar)
            else:
                no_usar = optimos[i - 1][w]
                optimos[i][w] = no_usar
    return optimos

def c_solucion(P, W, optimos):
    solucion = []

    i = len(P)
    w = W
    while i > 0 and w > 0:
        espacio_restante = w - P[i-1]
        if espacio_restante >= 0:
            no_usar = optimos[i - 1][w]
            usar = optimos[i - 1][espacio_restante] + P[i - 1]
            if usar > no_usar:
                # usar
                solucion.append(P[i-1])
                i = i - 1
                w = espacio_restante
            else:
                # no usar
                i = i - 1
                w = w
        else:
            # no usar
            i = i - 1
            w = w

    solucion.reverse()
    return solucion














import unittest

class TestBodegonDinamico(unittest.TestCase):

    def test_mesa_vacia_o_sin_grupos(self):
        """Si no hay grupos o la mesa no tiene lugar, no se sienta nadie."""
        self.assertEqual(bodegon_dinamico([], 10), [])
        self.assertEqual(bodegon_dinamico([5, 2], 0), [])

    def test_mio(self):
        P = [3, 1, 5, 2, 8]
        W = 10
        self.assertEqual(sum(bodegon_dinamico(P, W)), 10)

    def test_todos_entran(self):
        """Si la suma de todos los grupos es menor o igual a W, entran todos."""
        P = [2, 3, 4]
        W = 10
        self.assertEqual(sum(bodegon_dinamico(P, W)), 9)

    def test_eleccion_optima_simple(self):
        """Debe elegir la combinación que sume exactamente W."""
        P = [10, 20, 30]
        W = 40
        # 10 + 30 = 40. El 20 queda afuera.
        self.assertEqual([10, 30], bodegon_dinamico(P, W))

    def test_mejor_varios_pequenos_que_uno_grande(self):
        """Caso donde dos grupos pequeños suman más que uno grande solo."""
        P = [5, 8, 4]
        W = 10
        # 5 + 4 = 9 (es mejor que solo el 8)
        self.assertEqual(bodegon_dinamico(P, W), [5, 4])

    def test_orden_original(self):
        """El resultado debe respetar el orden en que aparecían en P."""
        P = [7, 2, 5, 8]
        W = 10
        # Opción A: 7 + 2 = 9
        # Opción B: 2 + 8 = 10 (Ganadora)
        # El orden debe ser [2, 8]
        self.assertEqual(bodegon_dinamico(P, W), [2, 8])

    def test_capacidad_justa(self):
        """Verifica que si un grupo ocupa toda la mesa, se lo elija si es lo máximo."""
        P = [15, 10, 5]
        W = 15
        # Aunque 10+5 también da 15, el algoritmo encontrará una solución de 15.
        # Ambas son válidas si sumas 15, pero el test espera una solución de suma 15.
        resultado = bodegon_dinamico(P, W)
        self.assertEqual(sum(resultado), 15)

if __name__ == '__main__':
    unittest.main()