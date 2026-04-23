
INICIO = 0
FIN = 1
PESO = 2

NINGUNA = -1

def scheduling(charlas):
    if not charlas:
        return []
    charlas.sort(key=lambda charla: charla[1]) # 0(n log n)
    optimos = {}
    calcular_optimos(charlas, optimos)
    calcular_resultado(charlas, optimos)
    return calcular_resultado(charlas, optimos)

def calcular_optimos(charlas, optimos):
    optimos[NINGUNA] = 0
    for i in range(0, len(charlas)): # O(n)
        optimo_sin_charla_i = optimos[i - 1]
        p = primera_charla_valida_antes_de(i, charlas) # O(log n)
        optimo_con_charla_i = charlas[i][PESO] + optimos[p]
        optimos[i] = max(optimo_con_charla_i, optimo_sin_charla_i)

def calcular_resultado(charlas, optimos):
    resultado = []
    i = len(charlas) - 1
    while i >= 0:
        p = primera_charla_valida_antes_de(i, charlas)
        if charlas[i][PESO] + optimos[p] > optimos[i-1]:
            resultado.append(charlas[i])
            i = p
        else:
            i = i - 1
    return resultado

def primera_charla_valida_antes_de(i, charlas):
    inicio_candidatos = 0
    fin_candidatos = i - 1
    candidato = NINGUNA

    while fin_candidatos > inicio_candidatos:
        centro = (fin_candidatos + inicio_candidatos) // 2
        if charlas[centro][FIN] <= charlas[i][INICIO]:
            candidato = centro
            inicio_candidatos = centro + 1
        else:
            fin_candidatos = centro - 1

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
        self.assertEqual(resultado, [])

    def test_una_sola_charla(self):
        """Si hay una sola charla, esa es la solución."""
        charlas = [(1, 5, 10)]
        resultado = scheduling(charlas)
        self.assertEqual(resultado, [(1, 5, 10)])

    def test_charlas_sin_solapamiento(self):
        """Si no se solapan, debería devolver todas las charlas."""
        charlas = [(1, 3, 10), (2, 4, 20), (5, 6, 30)]
        resultado = scheduling(charlas)
        self.assertCountEqual(resultado, charlas)

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

if __name__ == '__main__':
    unittest.main()
