def cambio(monedas, monto):
    if not monedas or not monto:
        return []
    optimos = c_optimos(monedas, monto)
    return c_solucion(monedas, monto, optimos)

def c_optimos(monedas, monto):
    optimos = [ 0 for _ in range(monto + 1) ]

    for w in range(monto + 1):
        minimo = monto # Todas de una unidad
        for moneda in monedas:
            if moneda > monto:
                continue
            cantidad = 1 + optimos[w - moneda]
            if cantidad <= minimo:
                minimo = cantidad
        optimos[monto] = minimo

    return optimos

def c_solucion(monedas, monto, optimos):
    solucion = []
    w = monto
    while w > 0:
        minimo = w  # Todas de una unidad
        moneda_usada = 1
        for moneda in monedas:
            if moneda > w:
                continue
            cantidad = 1 + optimos[w - moneda]
            if cantidad <= minimo:
                minimo = cantidad
                moneda_usada = moneda
        solucion.append(moneda_usada)
        w -= minimo * moneda_usada
    solucion.reverse()
    return solucion



import unittest

class TestCambioDinamico(unittest.TestCase):

    def test_caso_base_cero(self):
        """Si el monto es 0, no se deben devolver monedas."""
        self.assertEqual(cambio([1, 2, 5], 0), [])

    def test_moneda_unica(self):
        """Caso simple donde el monto coincide con una denominación."""
        self.assertEqual(cambio([1, 5, 10], 5), [5])

    def test_varias_monedas_simples(self):
        """Cambio estándar con múltiples monedas del mismo tipo."""
        resultado = cambio([1, 5, 10], 12)
        # Esperamos [10, 1, 1] (el orden no debería importar, pero la cantidad sí)
        self.assertEqual(len(resultado), 3)
        self.assertCountEqual(resultado, [10, 1, 1])

    def test_falla_de_algoritmo_greedy(self):
        """
        Este es el test crucial para Programación Dinámica.
        En un sistema [1, 3, 4], para dar 6 de cambio:
        - Greedy daría: 4 + 1 + 1 (3 monedas)
        - Dinámica debe dar: 3 + 3 (2 monedas)
        """
        resultado = cambio([1, 3, 4], 6)
        #self.assertEqual(len(resultado), 2)
        self.assertCountEqual(resultado, [3, 3])

    def test_sistema_no_canonico(self):
        """Otro caso donde el algoritmo voraz falla."""
        # Para 15, greedy haría 10 + 1 + 1 + 1 + 1 + 1 (6 monedas)
        # Dinámica debe hacer 9 + 6 (2 monedas)
        resultado = cambio([1, 6, 9], 15)
        self.assertEqual(len(resultado), 2)
        self.assertCountEqual(resultado, [9, 6])

    def test_monto_grande(self):
        """Verifica que el algoritmo maneje montos moderadamente altos."""
        resultado = cambio([1, 5, 10, 25], 63)
        # 25 + 25 + 10 + 1 + 1 + 1 (6 monedas)
        self.assertEqual(len(resultado), 6)
        self.assertCountEqual(resultado, [25, 25, 10, 1, 1, 1])

    def test_sin_solucion(self):
        """
        Si no es posible dar el cambio con las monedas provistas,
        el comportamiento esperado suele ser retornar None o una lista vacía
        (dependiendo de la especificación, aquí asumimos None o similar).
        """
        # Si solo hay monedas de 2 y 5, no se puede dar 3.
        self.assertEqual(cambio([2, 5], 3), None)

    def test_monedas_desordenadas(self):
        """El algoritmo no debería depender de que el array esté ordenado."""
        resultado = cambio([10, 1, 5], 11)
        self.assertCountEqual(resultado, [10, 1])

if __name__ == '__main__':
    unittest.main()