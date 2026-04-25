
# Ecuación de recurrencia:
#
# OPT(0) = g_0
# OPT(1) = max(g_0, g_1)
#
# OPT(n) = max( OPT(n-2) + g_n , OPT(n-1) )
#
# Complejidad: 0(n) con n el tamaño de ganancias
def lunatico(ganancias):
    if not ganancias:
        return []
    if len(ganancias) == 1:
        return [0]
    if len(ganancias) == 2:
        return [0] if ganancias[0] > ganancias[1] else [1]

    ganancias_sin_la_primera = ganancias[1:] # O(n)
    ganancias_sin_la_ultima = ganancias[:-1] # O(n)

    optimos_sin_la_primera = c_optimos(ganancias_sin_la_primera) # O(n)
    optimos_sin_la_ultima = c_optimos(ganancias_sin_la_ultima) # O(n)

    if optimos_sin_la_primera[-1] > optimos_sin_la_ultima[-1]:
        return [i + 1 for i in c_solucion(ganancias_sin_la_primera, optimos_sin_la_primera)]
    else:
        return c_solucion(ganancias_sin_la_ultima, optimos_sin_la_ultima)


def c_optimos(ganancias):
    if len(ganancias) == 0:
        return []
    elif len(ganancias) == 1:
        return [ganancias[0]]

    optimos = [ 0 for _ in range(len(ganancias)) ] # O(n)
    optimos[0] = ganancias[0]
    optimos[1] = max(ganancias[0], ganancias[1])
    for n in range(2, len(ganancias)): # O(n)
        si_robo_la_ultima = ganancias[n] + optimos[n-2]
        si_no_robo_la_ultima = optimos[n-1]
        optimos[n] = max(si_robo_la_ultima, si_no_robo_la_ultima)
    return optimos


def c_solucion(ganancias, optimos):
    solucion = []
    n = len(optimos) - 1
    while n >= 0: # O(n)
        if n == 0:
            solucion.append(0)
            break
        elif n == 1:
            solucion.append(1 if ganancias[1] > ganancias[0] else 0)
            break
        else:
            si_robo_la_ultima = ganancias[n] + optimos[n - 2]
            si_no_robo_la_ultima = optimos[n - 1]
            if si_robo_la_ultima >= si_no_robo_la_ultima:
                solucion.append(n)
                n = n - 2
            else:
                n = n - 1
    solucion.reverse() # O(n)
    return solucion



















def lunatico_verificada(ganancias):
    n = len(ganancias)

    # Casos base iniciales
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0] if ganancias[0] >= ganancias[1] else [1]

    def robar_lineal(start, end):
        """
        Resuelve el problema del ladrón de casas para un arreglo lineal
        desde el índice 'start' hasta 'end' (inclusive).
        """
        L = end - start + 1
        dp = [0] * L

        # Casos base para el subproblema lineal
        dp[0] = ganancias[start]
        dp[1] = max(ganancias[start], ganancias[start + 1])

        # Llenamos el arreglo de DP
        for i in range(2, L):
            dp[i] = max(dp[i - 1], dp[i - 2] + ganancias[start + i])

        # Reconstrucción de la solución (qué casas robamos)
        casas = []
        i = L - 1
        while i >= 0:
            if i == 0:
                casas.append(start)
                break
            if i == 1:
                # Si dp[1] es igual a dp[0], significa que la ganancia de la
                # primera casa era mejor o igual, así que no robamos la segunda.
                if dp[1] == dp[0]:
                    casas.append(start)
                else:
                    casas.append(start + 1)
                break

            # Si el valor actual es igual al anterior, significa que
            # NO robamos la casa actual.
            if dp[i] == dp[i - 1]:
                i -= 1
            else:
                # Si el valor cambió, SÍ robamos la casa actual
                # y saltamos la adyacente anterior.
                casas.append(start + i)
                i -= 2

        # Invertimos la lista porque reconstruimos de atrás hacia adelante
        return dp[-1], casas[::-1]

    # Evaluamos los dos escenarios posibles
    ganancia1, casas1 = robar_lineal(0, n - 2)
    ganancia2, casas2 = robar_lineal(1, n - 1)

    # El Lunático se queda con el plan que le dé mayor ganancia
    if ganancia1 >= ganancia2:
        return casas1
    else:
        return casas2


import unittest
import random


# Asumimos que aquí importas tus funciones.
# from tu_modulo import lunatico, lunatico_verificada

def calcular_ganancia(ganancias, casas_robadas):
    """
    Función auxiliar para calcular cuánta ganancia real nos da
    una lista de casas robadas. Útil por si hay empates óptimos.
    """
    return sum(ganancias[i] for i in casas_robadas)


import unittest
import random

def calcular_ganancia(ganancias, casas_robadas):
    return sum(ganancias[i] for i in casas_robadas)

class TestLunatico(unittest.TestCase):

    def setUp(self):
        random.seed(42)

    def verificar_resultado(self, ganancias):
        """Método auxiliar para reducir repetición de lógica de aserción."""
        res_test = lunatico(ganancias)
        res_verificado = lunatico_verificada(ganancias)

        ganancia_test = calcular_ganancia(ganancias, res_test)
        ganancia_verificada = calcular_ganancia(ganancias, res_verificado)

        self.assertEqual(ganancia_test, ganancia_verificada,
                         f"La ganancia total no coincide en: {ganancias}")
        # Descomentar si el orden de los índices debe ser idéntico
        # self.assertEqual(res_test, res_verificado)

    # --- Casos Base y Pequeños ---

    def test_vacio(self):
        self.verificar_resultado([])

    def test_una_casa(self):
        self.verificar_resultado([10])

    def test_dos_casos_orden_asc(self):
        self.verificar_resultado([10, 20])

    def test_dos_casos_orden_desc(self):
        self.verificar_resultado([20, 10])

    def test_tres_casos_circular(self):
        self.verificar_resultado([10, 20, 30])

    # --- Casos de Borde y Específicos ---

    def test_ganancias_cero(self):
        self.verificar_resultado([0, 0, 0, 0, 0])

    def test_ganancias_iguales(self):
        self.verificar_resultado([10, 10, 10, 10])

    def test_alternados_convenientes(self):
        # Conviene saltar de a pares
        self.verificar_resultado([1, 100, 1, 100, 1])

    def test_trampa_circular(self):
        # 1ro y último son vecinos, no pueden elegirse juntos
        self.verificar_resultado([100, 1, 1, 100, 1])

    def test_patron_repetitivo(self):
        self.verificar_resultado([5, 1, 2, 5, 1, 2, 5])

    def test_volumen_aleatorio_moderado(self):
        # 10 pruebas con arreglos de 1,000 casas
        for _ in range(10):
            ganancias = [random.randint(0, 1000) for _ in range(1000)]

            resultado_test = lunatico(ganancias)
            resultado_verificado = lunatico_verificada(ganancias)

            ganancia_test = calcular_ganancia(ganancias, resultado_test)
            ganancia_verificada = calcular_ganancia(ganancias, resultado_verificado)

            self.assertEqual(ganancia_test, ganancia_verificada)

    def test_volumen_aleatorio_masivo(self):
        # 2 pruebas con arreglos de 100,000 casas para medir estrés y recursión/memoria
        for _ in range(2):
            ganancias = [random.randint(10, 5000) for _ in range(100000)]

            resultado_test = lunatico(ganancias)
            resultado_verificado = lunatico_verificada(ganancias)

            ganancia_test = calcular_ganancia(ganancias, resultado_test)
            ganancia_verificada = calcular_ganancia(ganancias, resultado_verificado)

            self.assertEqual(ganancia_test, ganancia_verificada)


if __name__ == '__main__':
    unittest.main()











"""
def lunatico(ganancias):
    optimos = c_optimos(ganancias)
    return c_solucion(ganancias, optimos)


def c_optimos(ganancias):
    optimos = [ [ None for _ in range(len(ganancias)) ] for _ in range(len(ganancias)) ]
    # Casos base: pares (inicio, fin) con (fin - inicio) < 3
    for inicio in range(len(ganancias)):
        for fin in range(len(ganancias)):
            if fin < inicio:
                continue # la matriz es triangular superior
            else:
                distancia = fin - inicio
                if distancia == 0:
                    optimos[inicio][fin] = ganancias[inicio]
                if distancia == 1:
                    optimos[inicio][fin] = max(ganancias[inicio], ganancias[fin])
                elif distancia == 2:
                    ganancia_con_extremos = ganancias[inicio] + ganancias[fin]
                    ganancia_con_medio = ganancias[inicio+1]
                    optimos[inicio][fin] = ganancia_con_extremos if ganancia_con_extremos > ganancia_con_medio else ganancia_con_medio
    # Casos recurrentes: pares (inicio, fin) con (fin - inicio) >= 3
    for inicio in range(len(ganancias)):
        for fin in range(len(ganancias)):
            if fin < inicio:
                continue
            else:
                distancia = fin - inicio
                if distancia > 2:
                    si_robo_el_ultimo = optimos[inicio+1][fin-1] + ganancias[fin]
                    si_no_robo_el_ultimo = optimos[inicio][fin-1]
                    optimos[inicio][fin] = max(si_robo_el_ultimo, si_no_robo_el_ultimo)
    return optimos


def c_solucion(ganancias, optimos):
    solucion = []
    inicio = 0
    fin = len(ganancias) - 1
    while inicio <= fin:
        distancia = fin - inicio
        if distancia == 0:
            solucion.append(inicio)
            break
        elif distancia == 1:
            solucion.append(inicio if ganancias[inicio] > ganancias[fin] else fin)
            break
        elif distancia == 2:
            ganancia_con_extremos = ganancias[inicio] + ganancias[fin]
            ganancia_con_medio = ganancias[inicio + 1]
            solucion.append(ganancia_con_extremos if ganancia_con_extremos > ganancia_con_medio else ganancia_con_medio)
            break
        else:
            si_robo_el_ultimo = optimos[inicio + 1][fin - 1] + ganancias[fin]
            si_no_robo_el_ultimo = optimos[inicio][fin - 1]
            if si_robo_el_ultimo > si_no_robo_el_ultimo:
                solucion.append(fin)
                inicio = inicio + 1
                fin = fin - 1
            else:
                fin = fin - 1
    return solucion
"""