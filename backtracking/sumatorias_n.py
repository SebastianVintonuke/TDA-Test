
def sumatorias_n(lista, n):
    resultados = []
    sumatorias_n_rec(lista, n, 0, [], 0, resultados)
    return resultados

def sumatorias_n_rec(lista, n, indice, incluidos, sumatoria, resultados):
    if sumatoria == n:
        resultados.append(incluidos[:])
        return
    if len(lista) == indice:
        return
    # poda ya me pase
    if sumatoria > n:
        return

    candidato = lista[indice]
    # pruebo poner
    incluidos.append(candidato)
    sumatoria += candidato
    sumatorias_n_rec(lista, n, indice + 1, incluidos, sumatoria, resultados)
    sumatoria -= candidato
    incluidos.pop()
    # pruebo no poner
    sumatorias_n_rec(lista, n, indice + 1, incluidos, sumatoria, resultados)
    return





import unittest

class TestSumatoriasN(unittest.TestCase):

    def test_caso_basico(self):
        """Caso estándar con múltiples combinaciones posibles."""
        lista = [1, 2, 3, 4]
        n = 5
        resultado = sumatorias_n(lista, n)
        # Las combinaciones que suman 5 son [1, 4] y [2, 3]
        esperado = [[1, 4], [2, 3]]
        self.assertCountEqual([tuple(sorted(x)) for x in resultado], [tuple(sorted(x)) for x in esperado])

    def test_elementos_repetidos(self):
        """Debe manejar correctamente si la lista tiene números iguales."""
        lista = [1, 2, 1]
        n = 2
        resultado = sumatorias_n(lista, n)
        # Puede ser el '2' solo, o el primer '1' con el segundo '1'
        esperado = [[2], [1, 1]]
        self.assertCountEqual([tuple(sorted(x)) for x in resultado], [tuple(sorted(x)) for x in esperado])

    def test_sin_solucion(self):
        """Debe devolver lista vacía si ninguna combinación suma n."""
        self.assertEqual(sumatorias_n([10, 20, 30], 5), [])
        self.assertEqual(sumatorias_n([5, 5], 11), [])

    def test_lista_vacia(self):
        """Una lista vacía no debería encontrar sumas (a menos que n sea 0)."""
        self.assertEqual(sumatorias_n([], 10), [])

    def test_n_es_cero(self):
        """Técnicamente, el subconjunto vacío suma 0."""
        # Dependiendo de la cátedra, esto podría devolver [[]] o []
        # Generalmente en backtracking de este tipo se espera [[]]
        self.assertEqual(sumatorias_n([1, 2, 3], 0), [[]])

    def test_usar_todos_los_elementos(self):
        """Caso donde la suma es exactamente el total de la lista."""
        lista = [1, 1, 1]
        n = 3
        self.assertEqual(sumatorias_n(lista, n), [[1, 1, 1]])

if __name__ == '__main__':
    unittest.main()