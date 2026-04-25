

# Ecuación de Recurrencia:
#                OPT(0) = 0
#                OPT(1) = V_1
#
#                OPT(n) = max( OPT(p) + V_n, OPT(n-1) ) ; p siendo el primer índice compatible anterior a n
#
# Complejidad: O(n log n), dada por el ordenamiento de las charlas por horario de fin

INICIO = 0
FIN = 1
VALOR = 2

def scheduling(charlas):
    if not charlas:
        return []
    charlas.sort(key=lambda charla: charla[FIN]) # O(n log n)
    optimos = c_optimos(charlas)
    return c_solucion(charlas, optimos)


def c_optimos(charlas):
    optimos = [ None for _ in range(len(charlas) + 1)]
    optimos[0] = 0
    optimos[1] = charlas[0][VALOR]
    for i in range(2, len(optimos)): # O(n)
        p = primera_valida_anterior(i-1, charlas)
        si_doy_la_charla = optimos[p] + charlas[i-1][VALOR]
        si_no_doy_la_charla = optimos[i-1]
        optimos[i] = max(si_doy_la_charla, si_no_doy_la_charla)
    return optimos


def c_solucion(charlas, optimos):
    solucion = []
    i = len(optimos) - 1
    while i >= 0: # O(n)
        if i == 0:
            break
        elif i == 1:
            solucion.append(charlas[i-1])
            break
        p = primera_valida_anterior(i-1, charlas)
        si_doy_la_charla = optimos[p] + charlas[i-1][VALOR]
        si_no_doy_la_charla = optimos[i-1]
        if si_doy_la_charla > si_no_doy_la_charla:
            solucion.append(charlas[i-1])
            i = p
        else:
            i = i-1
    solucion.reverse()
    return solucion


def primera_valida_anterior(i, charlas):
    inicio = 0
    fin = i - 1
    candidato = 0
    while inicio <= fin: # O(log n) (búsqueda binaria)
        centro = inicio + (fin - inicio) // 2
        if charlas[centro][FIN] <= charlas[i][INICIO]:
            candidato = centro + 1 # +1 para transformarlo en indice en optimos
            inicio = centro + 1
        else:
            fin = centro - 1
    return candidato















import unittest

class TestWeightedScheduling(unittest.TestCase):

    def test_tardos(self):
        charlas = [
            (0, 3, 2),
            (1, 5, 4),
            (4, 6, 4),
            (2, 8, 7),
            (7, 10, 2),
            (8, 11, 1)
        ]
        resultado = scheduling(charlas)
        self.assertEqual(resultado, [(0, 3, 2), (4, 6, 4), (7, 10, 2)])

    def test_una_sola_charla(self):
        """Si hay una sola charla, esa es la solución."""
        charlas = [(1, 5, 10)]
        resultado = scheduling(charlas)
        self.assertEqual(resultado, [(1, 5, 10)])

    def test_charlas_sin_solapamiento(self):
        """Si no se solapan, debería devolver todas las charlas."""
        charlas = [(1, 3, 10), (2, 4, 20), (5, 6, 30)]
        resultado = scheduling(charlas)
        self.assertCountEqual(resultado, [(2, 4, 20), (5, 6, 30)])

    def test_eleccion_por_valor_maximo(self):
        """
        Caso donde conviene una charla corta y valiosa sobre una larga.
        Charla A: (1, 10, 50)
        Charla B: (2, 3, 100) -> Mejor esta sola.
        """
        charlas = [(1, 10, 50), (2, 3, 100)]
        resultado = scheduling(charlas)
        self.assertEqual(resultado, [(2, 3, 100)])

    def test_combinacion_optima(self):
        """
        Caso donde dos charlas chicas superan a una grande.
        A: (1, 4, 10)
        B: (3, 6, 15)  <-- Esta se solapa con A y C
        C: (5, 8, 10)
        Optimo: A + C = 20, que es mejor que B solo (15).
        """
        charlas = [(1, 4, 10), (3, 6, 15), (5, 8, 10)]
        resultado = scheduling(charlas)
        self.assertCountEqual(resultado, [(1, 4, 10), (5, 8, 10)])

    def test_charlas_igual_valor(self):
        """Si valen lo mismo, debe elegir la combinación válida."""
        charlas = [(1, 3, 10), (2, 5, 10), (4, 6, 10)]
        resultado = scheduling(charlas)
        # Optimo es (1, 3) y (4, 6) sumando 20.
        self.assertEqual(len(resultado), 2)
        self.assertEqual(sum(c[2] for c in resultado), 20)

    def test_reversa_ejemplo_corrector(self):
        """Caso donde la suma de pequeñas supera a una grande y hay limites exactos."""
        charlas = [
            (3, 14, 7),
            (1, 6, 2),
            (7, 11, 4),
            (11, 16, 2)
        ]
        # El optimo es 2+4+2 = 8, no 7.
        resultado = scheduling(charlas)
        self.assertEqual(sum(c[2] for c in resultado), 8)
        self.assertEqual(resultado, [(1, 6, 2), (7, 11, 4), (11, 16, 2)])

    def test_reversa_varias_charlas(self):
        """Caso de los logs con muchas charlas consecutivas."""
        charlas = [
            (4, 8, 5), (9, 11, 4), (13, 17, 5),
            (11, 12, 1), (14, 16, 2), (16, 17, 4)
        ]
        # Tu actual: (4,8,5) + (9,11,4) + (13,17,5) = 14
        # El esperado: (4,8,5) + (9,11,4) + (11,12,1) + (14,16,2) + (16,17,4) = 16
        resultado = scheduling(charlas)
        self.assertEqual(sum(c[2] for c in resultado), 16)
        self.assertEqual(resultado, [(4, 8, 5), (9, 11, 4), (11, 12, 1), (14, 16, 2), (16, 17, 4)])

if __name__ == '__main__':
    unittest.main()
