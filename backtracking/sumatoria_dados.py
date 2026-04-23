
DADO_MIN = 1
DADO_MAX = 6

def sumatoria_dados(n, s):
    min_dados = s // DADO_MAX
    if min_dados * DADO_MAX < s:
        min_dados += 1

    # Tengo menos dados de los que necesito para esa sumatoria
    if n < min_dados:
        return []

    resultados = []
    sumatoria_dados_rec(n, s, [], 0, resultados)
    return resultados

def sumatoria_dados_rec(dados_restantes, sumatoria_objetivo, tiradas, sumatoria, resultados):
    if dados_restantes == 0:
        if sumatoria == sumatoria_objetivo:
            resultados.append(tiradas[:])
        return

    sumatoria_faltante = sumatoria_objetivo - sumatoria

    # Ya no llego ni aunque saque los mejores dados
    if dados_restantes * DADO_MAX < sumatoria_faltante:
        return

    # Ya me paso aunque saque los peores dados
    if dados_restantes * DADO_MIN > sumatoria_faltante:
        return

    for tirada in range(DADO_MIN, DADO_MAX + 1):
        tiradas.append(tirada)
        sumatoria_dados_rec(dados_restantes - 1, sumatoria_objetivo, tiradas, sumatoria + tirada, resultados)
        tiradas.pop()
    return





import unittest

class TestSumatoriaDados(unittest.TestCase):

    def test_caso_base_dos_dados(self):
        """Verifica el ejemplo clásico de n=2, s=7."""
        resultado = sumatoria_dados(2, 7)
        esperado = [[1, 6], [2, 5], [3, 4], [4, 3], [5, 2], [6, 1]]
        # Convertimos a sets de tuplas para comparar sin importar el orden de la lista principal
        self.assertCountEqual([tuple(x) for x in resultado], [tuple(x) for x in esperado])

    def test_un_solo_dado(self):
        """Con un dado, el resultado debe ser una lista con un único valor dentro de los límites."""
        self.assertEqual(sumatoria_dados(1, 3), [[3]])
        self.assertEqual(sumatoria_dados(1, 6), [[6]])
        self.assertEqual(sumatoria_dados(1, 7), []) # Imposible con un dado de 6 caras

    def test_suma_minima_y_maxima(self):
        """Verifica los límites físicos de los dados (todo 1s o todo 6s)."""
        self.assertEqual(sumatoria_dados(3, 3), [[1, 1, 1]])
        self.assertEqual(sumatoria_dados(3, 18), [[6, 6, 6]])

    def test_sumas_imposibles(self):
        """Verifica que devuelva lista vacía si la suma es inalcanzable."""
        self.assertEqual(sumatoria_dados(2, 1), [])  # Menor al mínimo (2)
        self.assertEqual(sumatoria_dados(2, 13), []) # Mayor al máximo (12)
        self.assertEqual(sumatoria_dados(4, 2), [])  # Demasiados dados para esa suma

    def test_cantidad_de_combinaciones(self):
        """Verifica que la cantidad de soluciones sea la correcta para n=3, s=10."""
        # El número de combinaciones para n=3, s=10 es 27
        resultado = sumatoria_dados(3, 10)
        self.assertEqual(len(resultado), 27)

if __name__ == '__main__':
    unittest.main()