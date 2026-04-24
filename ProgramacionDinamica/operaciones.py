

# Complejidad: O(n), especialmente dado por el cálculo lineal del costo de cada k
#
# Ecuación de recurrencia:
#
#                  OPT(k) = { min( OPT(N-1)+1, OPT(N//2)+1 )  si k % 2 == 0
#                           {      OPT(N-1)+1                 si k % 2 == 1
#
# Es decir si k es par, el minimo entre el óptimo de llegar a la mitad y multiplicar o llegar al anterior y sumar,
# si es impar no puedo llegar multiplicando, solo sumando
def operaciones(k):
    optimos = c_optimos(k)
    return c_solucion(optimos)

def c_optimos(k):
    optimos = [ -1 for _ in range(k + 1) ]
    optimos[0] = 0
    if len(optimos) == 1:
        return optimos
    optimos[1] = 1

    for n in range(2, k + 1): # O(n)
        llego_sumando = optimos[n - 1] + 1
        if n % 2 == 0:
            llego_multiplicando = optimos[n // 2] + 1
            optimos[n] = min(llego_sumando, llego_multiplicando)
        else:
            optimos[n] = llego_sumando
    return optimos

def c_solucion(optimos):
    solucion = []
    n = len(optimos) - 1

    while n >= 0: # O(n), (aunque solo si n < 4, si no, menos)
        if n == 0:
            break
        if n == 1:
            solucion.append("mas1")
            break

        llego_sumando = optimos[n - 1] + 1
        if n % 2 == 0:
            llego_multiplicando = optimos[n // 2] + 1
            if llego_sumando < llego_multiplicando:
                solucion.append("mas1")
                n = n - 1
            else:
                solucion.append("por2")
                n = n // 2
        else:
            solucion.append("mas1")
            n = n - 1
    solucion.reverse()
    return solucion













import unittest

class TestOperacionesK(unittest.TestCase):

    def test_caso_base_cero(self):
        """Desde 0 a 0 no se requieren operaciones."""
        self.assertEqual(operaciones(0), [])

    def test_caso_uno(self):
        """Desde 0 a 1 la única opción es sumar 1."""
        # 0 + 1 = 1
        self.assertEqual(operaciones(1), ['mas1'])

    def test_numero_par_pequeno(self):
        """Desde 0 a 2: +1, *2 es mejor que +1, +1."""
        # 0 + 1 = 1; 1 * 2 = 2 (2 operaciones)
        # 0 + 1 = 1; 1 + 1 = 2 (2 operaciones, pero suele priorizarse el doble)
        res = operaciones(2)
        self.assertEqual(len(res), 2)
        self.assertEqual(res, ['mas1', 'por2'])

    def test_numero_impar_pequeno(self):
        """Desde 0 a 3: +1, *2, +1 o +1, +1, +1."""
        # 0+1=1, 1*2=2, 2+1=3 (3 ops)
        res = operaciones(3)
        self.assertEqual(len(res), 3)
        self.assertEqual(res, ['mas1', 'por2', 'mas1'])

    def test_potencia_de_dos(self):
        """Para K=4, el camino óptimo es +1, *2, *2."""
        # 0+1=1, 1*2=2, 2*2=4 (3 ops)
        self.assertEqual(operaciones(4), ['mas1', 'por2', 'por2'])

    def test_caso_seis(self):
        """Para K=6, el camino óptimo es +1, *2, +1, *2 o +1, +1, +1, *2?"""
        # Opción A: 0+1=1, 1+1=2, 2+1=3, 3*2=6 (4 ops)
        # Opción B: 0+1=1, 1*2=2, 2+1=3, 3*2=6 (4 ops)
        # Ambas son válidas por ser mínima cantidad (4)
        res = operaciones(6)
        self.assertEqual(len(res), 4)
        # Verificamos que las operaciones aplicadas den 6
        valor = 0
        for op in res:
            if op == 'mas1': valor += 1
            elif op == 'por2': valor *= 2
        self.assertEqual(valor, 6)

    def test_valor_mas_grande(self):
        """Para K=10, el camino óptimo tiene 5 operaciones."""
        # 0+1=1, 1*2=2, 2*2=4, 4+1=5, 5*2=10
        res = operaciones(10)
        self.assertEqual(len(res), 5)
        self.assertEqual(res, ['mas1', 'por2', 'por2', 'mas1', 'por2'])

if __name__ == '__main__':
    unittest.main()
