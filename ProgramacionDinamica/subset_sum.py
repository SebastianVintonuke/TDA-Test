
# Ecuación de Recurrencia:
#       OPT(0, v) = { numeros[0]  ; si numeros[0] <= v
#                   { 0           ; si numeros[0] >  v
#
#       OPT(n, v) = { max( numeros[n] + OPT(n-1, v - numeros[n]), OPT(n-1, v) )  ; si v - numeros[n] >= 0
#                   { OPT(n-1, v)                                                ; si v - numeros[n] <  0
#
# Complejidad: O(n * v) = O(n * 2^m)    ; con n la cantidad de elementos

def subset_sum(elementos, v):
    if not elementos:
        return []
    optimos = c_optimos(elementos, v)
    return c_solucion(elementos, v, optimos)

def c_optimos(numeros, v):
    optimos = [ [ None for _ in range(v+1) ] for _ in range(len(numeros)) ]

    for objetivo in range(v+1):
        optimos[0][objetivo] = numeros[0] if numeros[0] <= objetivo else 0

    for numero in range(1, len(numeros)):
        for objetivo in range(v+1):
            si_no_lo_sumo = optimos[numero-1][objetivo]
            lo_que_me_falta = objetivo - numeros[numero]
            if lo_que_me_falta >= 0:
                si_lo_sumo = numeros[numero] + optimos[numero-1][lo_que_me_falta]
                optimos[numero][objetivo] = max(si_lo_sumo, si_no_lo_sumo)
            else:
                optimos[numero][objetivo] = si_no_lo_sumo
    return optimos

def c_solucion(numeros, v, optimos):
    solucion = []
    numero = len(numeros) - 1
    objetivo = v
    while numero >= 0 or objetivo >= 0:
        if numero == 0:
            if numeros[0] <= objetivo:
                solucion.append(numeros[0])
            break
        else:
            si_no_lo_sumo = optimos[numero - 1][objetivo]
            lo_que_me_falta = objetivo - numeros[numero]
            if lo_que_me_falta >= 0:
                si_lo_sumo = numeros[numero] + optimos[numero - 1][lo_que_me_falta]
                if si_lo_sumo >= si_no_lo_sumo:
                    solucion.append(numeros[numero])
                    objetivo = lo_que_me_falta
                    numero -= 1
                else:
                    numero -= 1
            else:
                numero -= 1
    solucion.reverse()
    return solucion







import unittest

class TestSubsetSum(unittest.TestCase):

    def test_capacidad_exacta(self):
        """El subconjunto suma exactamente V."""
        elementos = [3, 34, 4, 12, 5, 2]
        V = 9
        resultado = subset_sum(elementos, V)
        self.assertEqual(sum(resultado), 9)
        # Una solución válida es [4, 5] o [3, 4, 2]
        for x in resultado:
            self.assertIn(x, elementos)

    def test_aproximacion_maxima(self):
        """No hay suma exacta, debe devolver la mayor suma posible sin pasarse."""
        elementos = [10, 20, 30]
        V = 25
        resultado = subset_sum(elementos, V)
        self.assertEqual(sum(resultado), 20)

    def test_elementos_repetidos(self):
        """Debe manejar múltiples instancias del mismo valor."""
        elementos = [5, 5, 5, 10]
        V = 12
        resultado = subset_sum(elementos, V)
        self.assertEqual(sum(resultado), 10)
        # Puede ser [5, 5] o [10]
        self.assertTrue(len(resultado) >= 1)

    def test_elemento_mayor_que_v(self):
        """Elementos que superan V deben ser ignorados."""
        elementos = [100, 2, 3]
        V = 10
        resultado = subset_sum(elementos, V)
        self.assertEqual(sum(resultado), 5)
        self.assertNotIn(100, resultado)

    def test_todos_los_elementos(self):
        """La suma de todos es menor o igual a V."""
        elementos = [1, 2, 3, 4]
        V = 15
        resultado = subset_sum(elementos, V)
        self.assertEqual(sum(resultado), 10)
        self.assertCountEqual(resultado, [1, 2, 3, 4])

    def test_v_cero(self):
        """Si la capacidad es 0, el resultado es vacío."""
        elementos = [1, 2, 3]
        V = 0
        self.assertEqual(subset_sum(elementos, V), [])

    def test_lista_vacia(self):
        """Si no hay elementos, el resultado es vacío."""
        self.assertEqual(subset_sum([], 10), [])

    def test_sin_solucion_menor_que_v(self):
        """Todos los elementos son mayores que V."""
        elementos = [20, 30, 40]
        V = 10
        self.assertEqual(subset_sum(elementos, V), [])

    def test_caso_complejo(self):
        """Caso donde elegir el elemento más grande inicialmente no es óptimo."""
        # Si fuera greedy, elegiría 15 y llegaría a 15.
        # Óptimo es 8 + 8 + 4 = 20.
        elementos = [15, 8, 8, 4, 1]
        V = 20
        resultado = subset_sum(elementos, V)
        self.assertEqual(sum(resultado), 20)

    def test_v_muy_pequeno(self):
        """V es menor que el elemento más pequeño."""
        elementos = [5, 10, 15]
        V = 3
        self.assertEqual(subset_sum(elementos, V), [])

if __name__ == '__main__':
    unittest.main()