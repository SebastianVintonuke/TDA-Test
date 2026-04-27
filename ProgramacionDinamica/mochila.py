
# Ecuación de recurrencia:
#
#         OPT(0,W) = { V_o   si P_0 <= w
#                    { 0     si P_0 >  w
#
#         OPT(n,W) = { max( V_W + OPT(n-1, W-P_n), OPT(n-1, W) )    si W - P_n >= 0
#                    { OPT(n-1, W)                                  si W - P_n < 0
#
# Complejidad: O(n * W) = O(n * 2^m) ; con n la cantidad de elementos

VALOR = 0
PESO = 1

# cada elemento i de la forma (valor, peso)
def mochila(elementos, W):
    if not elementos:
        return []
    optimos = c_optimos(elementos, W)
    return c_solucion(elementos, W, optimos)

def c_optimos(elementos, W):
    optimos = [ [ None for _ in range(W+1) ] for _ in range(len(elementos)) ]
    # Lleno la primera fila, si entra lo llevo, si no, no
    for capacidad in range(W+1):
        optimos[0][capacidad] = elementos[0][VALOR] if elementos[0][PESO] <= capacidad else 0
    # Lleno el resto de elementos, si no lo llevo, llevo lo que ya tenia con el mismo peso, si lo llevo, llevo el valor del elemento y el optimo de la capacidad sin el peso del elemento
    for elemento in range(1,len(elementos)):
        for capacidad in range(W+1):
            si_no_lo_uso = optimos[elemento - 1][capacidad]
            capacidad_restante = capacidad - elementos[elemento][PESO]
            if capacidad_restante >= 0: # el elemento entra
                si_lo_uso = elementos[elemento][VALOR] + optimos[elemento - 1][capacidad_restante]
                optimos[elemento][capacidad] = max(si_lo_uso, si_no_lo_uso)
            else:
                optimos[elemento][capacidad] = si_no_lo_uso
    return optimos

def c_solucion(elementos, W, optimos):
    solucion = []
    elemento = len(elementos) - 1
    capacidad = W

    while elemento >= 0 and capacidad >= 0:
        if elemento == 0:
            if elementos[0][PESO] <= capacidad:
                solucion.append(elementos[0])
            break
        else:
            si_no_lo_uso = optimos[elemento - 1][capacidad]
            capacidad_restante = capacidad - elementos[elemento][PESO]
            if capacidad_restante >= 0: # el elemento entra
                si_lo_uso = elementos[elemento][VALOR] + optimos[elemento - 1][capacidad_restante]
                if si_lo_uso >= si_no_lo_uso:
                    solucion.append(elementos[elemento])
                    capacidad = capacidad_restante
            elemento = elemento - 1

    solucion.reverse()
    return solucion








import unittest


class TestMochila(unittest.TestCase):

    def test_caso_simple_reconstruccion(self):
        """
        Matriz esperada (3 elementos, Capacidad 5):
        Items: (v2, p3), (v3, p2), (v4, p4)
        """
        elementos = [(2, 3), (3, 2), (4, 4)]
        W = 5
        # Explicación:
        # (2,3) + (3,2) = Valor 5, Peso 5.
        # (4,4) solo entra solo = Valor 4.
        # Ganancia máxima: 5
        resultado = mochila(elementos, W)

        valor_total = sum(e[0] for e in resultado)
        self.assertEqual(valor_total, 5)
        self.assertIn((2, 3), resultado)
        self.assertIn((3, 2), resultado)

    def test_descarte_por_peso(self):
        """Un elemento tiene mucho valor pero excede la capacidad."""
        elementos = [(10, 6), (5, 4), (4, 3)]
        W = 5
        # El de valor 10 no entra. Debe elegir el de (5, 4).
        resultado = mochila(elementos, W)
        self.assertEqual(sum(e[0] for e in resultado), 5)
        self.assertEqual(resultado, [(5, 4)])

    def test_empate_valores(self):
        """Dos formas de llegar al mismo valor, debe elegir una válida."""
        elementos = [(5, 2), (5, 2)]
        W = 3
        # Solo entra uno.
        resultado = mochila(elementos, W)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(sum(e[0] for e in resultado), 5)

    def test_capacidad_justa(self):
        """El elemento entra exactamente en el límite."""
        elementos = [(10, 5)]
        W = 5
        self.assertEqual(mochila(elementos, W), [(10, 5)])

    def test_mochila_vacia_capacidad_pequena(self):
        """Capacidad mínima con elementos que no entran."""
        elementos = [(2, 2), (3, 2)]
        W = 1
        self.assertEqual(mochila(elementos, W), [])

    def test_mismos_pesos(self):
        """
        Error observado: AssertionError: [(1, 1), (3, 1)] != [(2, 1), (3, 1)]
        Ingeniería inversa: Capacidad W=2. Elementos con peso 1.
        Debe elegir los dos de mayor valor.
        """
        elementos = [(1, 1), (2, 1), (3, 1)]
        W = 2
        resultado = mochila(elementos, W)
        # El error sugiere que tu código olvidó el (2, 1) y tomó el (1, 1)
        self.assertEqual(resultado, [(2, 1), (3, 1)])

    def test_mismo_peso_y_valor(self):
        """
        Error observado: [(7, 7)] != [(3, 3), (7, 7)]
        Ingeniería inversa: W=10. Los elementos (3,3) y (7,7) suman 10.
        Tu código solo devolvió el (7,7).
        """
        elementos = [(3, 3), (7, 7)]
        W = 10
        resultado = mochila(elementos, W)
        self.assertEqual(resultado, [(3, 3), (7, 7)])

    def test_varios_pesos(self):
        """
        Error observado: [(1, 2), (9, 8)] != [(2, 3), (9, 8)]
        Ingeniería inversa: W=11. Elementos: (1,2), (2,3), (9,8).
        9+2=11 (v=11) vs 9+1=10 (v=10).
        """
        elementos = [(1, 2), (2, 3), (9, 8)]
        W = 11
        resultado = mochila(elementos, W)
        self.assertEqual(resultado, [(2, 3), (9, 8)])

    def test_pocos_elementos(self):
        """
        Error observado: [(8, 4)] != [(8, 4), (8, 4)]
        Ingeniería inversa: Hay elementos idénticos en la lista.
        La mochila debe permitir llevar ambos si la capacidad lo permite.
        """
        elementos = [(8, 4), (8, 4)]
        W = 8
        resultado = mochila(elementos, W)
        self.assertEqual(resultado, [(8, 4), (8, 4)])


if __name__ == '__main__':
    unittest.main()