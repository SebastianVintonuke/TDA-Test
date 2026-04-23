"""
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
"""
"""
def fibonacci(n):
    resultados = { 0: 0, 1: 1 }

    def _fibbonacci(n):
        if n in resultados:
            return resultados[n]
        else:
            resultados[n] = _fibbonacci(n - 1) + _fibbonacci(n - 2)
            return resultados[n]

    return _fibbonacci(n)
"""
"""
def fibonacci(n):
    resultados = {}
    resultados[0] = 0
    resultados[1] = 1

    for n in range(2, n + 1):
        resultados[n] = resultados[n - 1] + resultados[n - 2]

    return resultados[n]
"""
def fibonacci(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        actual = 1
        anterior = 1

    for n in range (2, n + 1):
        temp = actual
        actual += anterior
        anterior = temp

    return actual




import unittest

class TestFibonacciDinamico(unittest.TestCase):

    def test_casos_base(self):
        """Verifica n=0 y n=1 según la definición dada (ambos devuelven 1)."""
        self.assertEqual(fibonacci(0), 1)
        self.assertEqual(fibonacci(1), 1)

    def test_valores_intermedios(self):
        """Verifica la suma de los anteriores: F(2)=2, F(3)=3, F(4)=5."""
        self.assertEqual(fibonacci(2), 2) # 1 + 1
        self.assertEqual(fibonacci(3), 3) # 2 + 1
        self.assertEqual(fibonacci(4), 5) # 3 + 2
        self.assertEqual(fibonacci(5), 8) # 5 + 3

    def test_valor_grande(self):
        """Verifica un valor más alto para asegurar que la suma se mantiene correcta."""
        # La secuencia sería: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
        self.assertEqual(fibonacci(10), 89)

if __name__ == '__main__':
    unittest.main()