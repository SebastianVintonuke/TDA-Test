# Complejidad: O(n log n), el ordenamiento es el término dominante

# ¿El algoritmo implementado encuentra siempre la solución óptima?
# No, depende del sistema monetario

# Justificar si es óptimo, o dar un contraejemplo.
# si el sistema monetario es [1, 5, 8] y el monto 10
# el algoritmo da [8, 1, 1], y la solución óptima es [5, 5]

# ¿Por qué se trata de un algoritmo Greedy?
# Porque toma una decision en base a un óptimo local para llegar a un óptimo global,
# en este caso, tomar la moneda más grande posible lleva a que se use la menor cantidad de monedas
def cambio(monedas, monto):
    monedas.sort(reverse=True) # O(n log(n))
    cambio = []
    for moneda in monedas: # O(n) * O(m) = O(n)
        if moneda <= monto:
            cantidad = monto // moneda
            monto -= cantidad * moneda
            for i in range(cantidad): # O(m)
                cambio.append(moneda)
    return cambio











import unittest


class TestCambioGreedy(unittest.TestCase):

    def test_cambio_simple(self):
        # Sistema estándar, monto exacto
        monedas = [1, 5, 10, 25]
        monto = 30
        resultado = cambio(monedas, monto)
        # Greedy debería elegir 25 y luego 5
        self.assertEqual(len(resultado), 2)
        self.assertIn(25, resultado)
        self.assertIn(5, resultado)

    def test_cambio_multiples_monedas(self):
        monedas = [1, 2, 5, 10]
        monto = 28
        resultado = cambio(monedas, monto)
        # Esperado: 10, 10, 5, 2, 1
        self.assertEqual(sum(resultado), 28)
        self.assertEqual(len(resultado), 5)
        self.assertEqual(resultado.count(10), 2)

    def test_monedas_desordenadas(self):
        # El algoritmo debe funcionar aunque el input no esté ordenado
        monedas = [5, 1, 10]
        monto = 16
        resultado = cambio(monedas, monto)
        # Esperado: 10, 5, 1
        self.assertEqual(sum(resultado), 16)
        self.assertEqual(len(resultado), 3)

    def test_monto_cero(self):
        self.assertEqual(cambio([1, 5, 10], 0), [])

    def test_contraejemplo_no_optimo_greedy(self):
        """
        Este test verifica si tu función sigue la lógica Greedy
        incluso cuando no es la mejor solución global.
        Para [1, 3, 4] y monto 6:
        - Greedy elige: 4, 1, 1 (3 monedas)
        - Óptimo real: 3, 3 (2 monedas)
        """
        monedas = [1, 3, 4]
        monto = 6
        resultado = cambio(monedas, monto)
        # Un algoritmo Greedy devolverá [4, 1, 1]
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado.count(4), 1)
        self.assertEqual(resultado.count(1), 2)

if __name__ == '__main__':
    unittest.main()