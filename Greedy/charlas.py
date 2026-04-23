

# Complejidad: O(n log n), el termino dominante es el ordenamiento comparativo
def _charlas(horarios):
    candidatos = sorted(horarios, key=lambda charla: charla[1], reverse=True) # O(n log n)
    charlas_tomadas = []
    while candidatos: # O(n)
        la_que_termina_primero = candidatos.pop()
        charlas_tomadas.append(la_que_termina_primero)
        candidatos = [charla for charla in candidatos if charla[0] >= la_que_termina_primero[1]]
    return charlas_tomadas

def charlas(horarios):
    candidatos = sorted(horarios, key=lambda c: c[1])  # O(n log n)
    charlas_tomadas = []
    for charla in candidatos:
        if not charlas_tomadas:
            charlas_tomadas.append(charla)
        else:
            ultima_charla_tomada = charlas_tomadas[-1]
            if empieza_despues_de(charla, ultima_charla_tomada):
                charlas_tomadas.append(charla)
    return charlas_tomadas

def empieza_despues_de(una_charla, otra_charla):
    return una_charla[0] >= otra_charla[1]


import unittest

class TestMaximizacionCharlas(unittest.TestCase):

    def test_charlas_sin_superposicion(self):
        # Todas se pueden dar
        h = [(1, 2), (3, 4), (5, 6)]
        resultado = charlas(h)
        self.assertEqual(len(resultado), 3)
        self.assertIn((1, 2), resultado)
        self.assertIn((3, 4), resultado)
        self.assertIn((5, 6), resultado)

    def test_charlas_superpuestas_totalmente(self):
        # Solo se puede elegir una, la que termina antes
        h = [(1, 10), (2, 3), (4, 5)]
        resultado = charlas(h)
        # Debería elegir (2, 3) y (4, 5). La de (1, 10) queda afuera.
        self.assertEqual(len(resultado), 2)
        self.assertIn((2, 3), resultado)
        self.assertIn((4, 5), resultado)

    def test_una_charla_larga_vs_varias_cortas(self):
        # Caso clásico: una charla dura todo el día, pero hay 3 chiquitas
        h = [(0, 10), (1, 2), (3, 4), (5, 6)]
        resultado = charlas(h)
        self.assertEqual(len(resultado), 3)
        self.assertNotIn((0, 10), resultado)

    def test_charlas_que_terminan_igual_que_empieza_la_otra(self):
        # Dependiendo de la convención, si termina a las 2, la otra puede empezar a las 2.
        # Generalmente en estos ejercicios se asume que f1 <= s2 es válido.
        h = [(1, 2), (2, 3), (3, 4)]
        resultado = charlas(h)
        self.assertEqual(len(resultado), 3)

    def test_arreglo_vacio_y_un_elemento(self):
        self.assertEqual(charlas([]), [])
        self.assertEqual(charlas([(1, 5)]), [(1, 5)])

    def test_desordenado_al_inicio(self):
        # Los horarios vienen desordenados en el input
        h = [(5, 7), (1, 3), (2, 5), (4, 6)]
        # Óptimo: (1, 3) y (4, 6) o (1, 3) y (5, 7)
        # Pero si elegís (2, 5) solo podrías dar esa y (5, 7)
        resultado = charlas(h)
        self.assertEqual(len(resultado), 2)

if __name__ == '__main__':
    unittest.main()


# (★★) Dada un aula/sala donde se pueden dar charlas. Las charlas tienen horario de inicio y fin.
# Implementar un algoritmo Greedy que reciba el arreglo de los horarios de las charlas,
# representando en tuplas los horarios de inicios de las charlas, y sus horarios de fin, e indique
# cuáles son las charlas a dar para maximizar la cantidad total de charlas.
# Indicar y justificar la complejidad del algoritmo implementado.

# Demostracion:
# Dado A el conjunto de charlas dado por mi algorítmo y O al conjunto de charlas optimo.
# No puedo demostrar que A = O, pero puedo demostrar que |A|=|O|, es decir,
# que contiene el mismo numero de charlas que cualquier solución óptima.
# Mi intención es demostrar que esta invariante se mantiene a lo largo de todo el algoritmo.
# llamo i_1, ... , i_k a las charlas en el orden que fueron agregadas a A, |A| = k,
# llamo j_1, ... , j_m a las charlas en el orden que fueron agregadas a O, |O| = m
# Quiero demostrar que k = m, y que para cualquier r, f(i_r) <= f(j_r)
# Demostración por Inducción:
# Para r = 1:
# Nuestro algoritmo toma la charla con menor tiempo de finalización por lo tanto es verdadero.
# Tomo como hipótesis inductiva que f(i_r) <= f(j_r) para r.
# Para r + 1:
# Como O es compatible f(j_r) <= f(j_{r+1}). combinando esto con la hipotesis inductiva
# podemos decir que: f(i_r) <= s(j_{r+1}) es decir que cuando el algoritmo elige i_r, j_r esta
# disponible, pero el algoritmo siempre elige la charla con el tiempo de fin mas corto y
# como j_r esta disponible, entonces f(i_r) <= f(j_r).
