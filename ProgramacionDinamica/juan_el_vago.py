
# Ecuación de Recurrencia:
#
#              OPT(0) = d_0
#              OPT(1) = max(d_0, d_1)
#
#              OPT(n) = max( OPT(n-2) + d_n, OPT(n-1) )
#
# Es decir, el maximo entre trabajar ese dia "OPT(n-2) + d_n", dado por el valor obtenido de ese día
# más el valor óptimo acumulado de los días trabajados exceptuando el anterior o
# no trabajar ese dia "OPT(n-1)" dado por el valor óptimo de los días trabajados exceptuando este ultimo
#
# Complejidad: O(n) dado especialmente por el costo de calcular el óptimo para cada día
def juan_el_vago(dias):
    if not dias:
        return []
    elif len(dias) == 1:
        return [0]
    optimos = c_optimos(dias)
    solucion = c_solucion(dias, optimos)
    return solucion

def c_optimos(dias):
    optimos = [ None for _ in range(len(dias)) ]
    optimos[0] = dias[0]
    optimos[1] = max(dias[0], dias[1])
    for n in range(2, len(dias)): # O(n)
        si_trabajo = dias[n] + optimos[n - 2]
        si_no_trabajo = optimos[n - 1]
        optimos[n] = max(si_trabajo, si_no_trabajo)
    return optimos

def c_solucion(dias, optimos):
    solucion = []
    n = len(dias) - 1
    while n >= 0: # O(n)
        if n == 0:
            solucion.append(0)
            break
        elif n == 1:
            solucion.append(0 if dias[0] > dias[1] else 1)
            break
        si_trabajo = dias[n] + optimos[n - 2]
        si_no_trabajo = optimos[n - 1]
        if si_trabajo > si_no_trabajo:
            solucion.append(n)
            n = n - 2
        else:
            n = n - 1
    solucion.reverse()
    return solucion




















import unittest

class TestJuanElVago(unittest.TestCase):

    def test_arreglo_vacio(self):
        """Si no hay ofertas, el resultado es una lista vacía."""
        self.assertEqual(juan_el_vago([]), [])

    def test_un_solo_dia(self):
        """Si hay un solo día, se trabaja ese día (índice 0)."""
        self.assertEqual(juan_el_vago([50]), [0])

    def test_dos_dias_adyacentes(self):
        """Debe elegir el índice del día con mayor monto."""
        self.assertEqual(juan_el_vago([10, 50]), [1])
        self.assertEqual(juan_el_vago([100, 20]), [0])

    def test_eleccion_alternada(self):
        """Debe devolver los índices de los días que suman el máximo monto."""
        # [10, 1, 1, 10] -> Conviene día 0 y día 3 (monto 20)
        self.assertEqual(juan_el_vago([10, 1, 1, 10]), [0, 3])

    def test_salteo_intermedio_complejo(self):
        """Verifica que elija la combinación óptima de índices."""
        # [5, 20, 10, 1, 30]
        # Opción A: 20 + 30 = 50 (índices 1 y 4)
        # Opción B: 5 + 10 + 30 = 45 (índices 0, 2, 4)
        self.assertEqual(juan_el_vago([5, 20, 10, 1, 30]), [1, 4])

    def test_no_hay_consecutivos(self):
        """Verifica que en el resultado no haya nunca dos índices seguidos."""
        res = juan_el_vago([10, 20, 30, 40, 50, 60])
        for i in range(len(res) - 1):
            self.assertTrue(res[i+1] - res[i] > 1, f"Días consecutivos detectados: {res[i]}, {res[i+1]}")

if __name__ == '__main__':
    unittest.main()