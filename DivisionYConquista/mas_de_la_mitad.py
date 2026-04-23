from collections import deque


def mas_de_la_mitad(arr):
    if not arr:
        return False
    return not not mas_de_la_mitad_rec(arr)

# Complejidad: O(n log(n))
# Teorema Maestro, A = 2, B = 2, C = 1
# Log_2(2) = 1 = C => n ^ C * log_2(n) = n log(n)
def mas_de_la_mitad_rec(arr):
    if len(arr) == 1:
        return arr[0]

    centro = len(arr) // 2
    izq = arr[:centro]
    der = arr[centro:]

    izq_candidato = mas_de_la_mitad_rec(izq)
    der_candidato = mas_de_la_mitad_rec(der)

    if izq_candidato == der_candidato:
        return izq_candidato

    izq_n = 0
    der_n = 0
    for e in arr:
        if e == izq_candidato:
            izq_n += 1
        elif e == der_candidato:
            der_n += 1

    if izq_n > der_n and izq_n > centro:
        return izq_candidato
    elif der_n > izq_n and der_n > centro:
        return der_candidato
    else:
        return None





import unittest

class TestElementoMayoritario(unittest.TestCase):

    def test_casos_positivos(self):
        # El 1 aparece 4 de 6 veces
        self.assertTrue(mas_de_la_mitad([1, 2, 3, 1, 1, 1]))
        # Caso base
        self.assertTrue(mas_de_la_mitad([1]))
        # El 5 aparece 3 de 5 veces
        self.assertTrue(mas_de_la_mitad([5, 5, 2, 1, 5]))
        # El mayoritario está en los extremos
        self.assertTrue(mas_de_la_mitad([2, 2, 2, 1, 1]))

    def test_casos_negativos(self):
        # Aparecen 2 de 5 veces (no es más de la mitad)
        self.assertFalse(mas_de_la_mitad([1, 2, 1, 2, 3]))
        # Aparece exactamente la mitad (2 de 4) -> debe ser False
        self.assertFalse(mas_de_la_mitad([1, 1, 2, 3]))
        # Arreglo vacío
        self.assertFalse(mas_de_la_mitad([]))
        # Todos distintos
        self.assertFalse(mas_de_la_mitad([1, 2, 3, 4, 5]))

    def test_casos_con_negativos_y_grandes(self):
        self.assertTrue(mas_de_la_mitad([-1, -1, 5, -1]))
        self.assertTrue(mas_de_la_mitad([1000, 2, 1000, 1000]))

    def test_falso_mayoritario_en_subarreglos(self):
        """
        Este caso es clave para División y Conquista:
        En [1, 1, 2, 2], en la primera mitad el 1 es mayoritario y
        en la segunda el 2 lo es, pero en el total ninguno lo es.
        """
        self.assertFalse(mas_de_la_mitad([1, 1, 2, 2]))

    def testUnoApareceLaMitad(self):
        """
        Caso crítico: n=4, el elemento aparece 2 veces.
        2 no es > (4/2). Debe devolver False.
        """
        arr = [1, 1, 2, 3]
        self.assertFalse(mas_de_la_mitad(arr), "Falló: n=4, aparece 2 veces y devolvió True")

    def testCasoDosMenosQueLaMitad(self):
        """
        Caso: n=5, el más frecuente aparece 2 veces.
        2 no es > (5/2 = 2.5). Debe devolver False.
        """
        arr = [1, 1, 2, 3, 4]
        self.assertFalse(mas_de_la_mitad(arr), "Falló: n=5, aparece 2 veces y devolvió True")

    def testNoMasDeMitadMuchosElementos(self):
        """
        Caso con más volumen pero sin mayoría absoluta.
        """
        arr = [1, 2, 1, 2, 1, 2]  # n=6, '1' aparece 3 veces. 3 no es > 3.
        self.assertFalse(mas_de_la_mitad(arr), "Falló: En n=6, un elemento con 3 apariciones no es mayoría")

    def testEmpateDeCandidatos(self):
        """
        Si hay dos candidatos fuertes pero ninguno supera la mitad.
        """
        arr = [1, 1, 1, 2, 2, 2]
        self.assertFalse(mas_de_la_mitad(arr), "Falló: Empate 3 a 3 en n=6")

    def testAlternanciaSinMayoria(self):
        """
        Muchos elementos intercalados.
        """
        arr = [1, 0, 1, 0, 1, 0, 1, 0]
        self.assertFalse(mas_de_la_mitad(arr))

if __name__ == '__main__':
    unittest.main()


"""
def mas_de_la_mitad(arr):
    return not not mas_de_la_mitad_rec(arr)[0]


def mas_de_la_mitad_rec(arr):
    if len(arr) == 1:
        return (arr[0], 1, [])

    centro = len(arr) // 2
    izq = arr[:centro]
    der = arr[centro:]

    (izq_candidato, izq_n, izq_resto) = mas_de_la_mitad_rec(izq)
    (der_candidato, der_n, der_resto) = mas_de_la_mitad_rec(der)

    if izq_candidato == der_candidato:
        return (izq_candidato, izq_n + der_n)

    resto = []
    for i in izq_resto + der_resto:
        if i == izq_candidato:
            izq_n += 1
        elif i == der_candidato:
            der_n += 1
        else:
            resto.append(i)

    if izq_n > der_n:
        return (izq_candidato, izq_n, resto)
    else:
        return (der_candidato, der_n, resto)
"""