# (★) Dada una escalera, y sabiendo que tenemos la capacidad de subir escalones de a 1 o 2 o 3 pasos, encontrar, utilizando programación dinámica, cuántas formas diferentes hay de subir la escalera hasta el paso n. Indicar y justificar la complejidad del algoritmo implementado. Ejemplos: n = 0 –> Debe devolver 1 (no moverse) n = 1 –> Debe devolver 1 (paso de 1) n = 2 –> Debe devolver 2 (dos pasos de 1, o un paso de 2) n = 3 –> Debe devolver 4 (un paso de 3, o tres pasos de 1, o un paso de 2 y uno de 1, o un paso de 1 y un paso de 2) n = 4 –> Debe devolver 7 n = 5 –> Debe devolver 13



# Ecuación de Recurrencia:
#
#                OPT(0) = 1
#                OPT(1) = 1
#                OPT(2) = 2
#                OPT(3) = 4
#
#                OPT(n) = OPT(n-3) + OPT(n-2) + OPT(n-1)
#
# Es decir, el costo de llegar a un escalon n es el costo sumado de llegar
# a todos los escalones desde los cuales puedo llegar a n con un solo paso
#
# Complejidad O(n), dado por recorrer todos los escalones en orden ascendente para calcular sus formas de llegar
def escalones(n):
    escalones = [1, 1, 2, 4]

    if n < 4:
        return escalones[n]
    else:
        for i in range(0, n - 3): # O(n)
            nuevo_escalon = escalones[1] + escalones[2] + escalones[3]
            nuevos_escalones = [ escalones[1], escalones[2], escalones[3], nuevo_escalon ]
            escalones = nuevos_escalones
    return escalones[-1]











import unittest

class TestEscalera(unittest.TestCase):

    def test_casos_base(self):
        """Verifica los valores iniciales definidos en el enunciado."""
        self.assertEqual(escalera(0), 1)  # No moverse
        self.assertEqual(escalera(1), 1)  # (1)
        self.assertEqual(escalera(2), 2)  # (1,1), (2)
        self.assertEqual(escalera(3), 4)  # (1,1,1), (1,2), (2,1), (3)

    def test_valores_intermedios(self):
        """Verifica la progresión para n=4 y n=5."""
        # n=4: 1+2+4 = 7
        self.assertEqual(escalera(4), 7)
        # n=5: 2+4+7 = 13
        self.assertEqual(escalera(5), 13)

    def test_valor_avanzado(self):
        """Verifica n=6 para asegurar que la lógica de triple suma se mantiene."""
        # n=6: 4+7+13 = 24
        self.assertEqual(escalera(6), 24)

    def test_n_negativo(self):
        """
        Opcional: Verifica que para escalones negativos no hay formas de subir.
        Dependiendo de tu implementación podría devolver 0 o lanzar error.
        """
        # Si decides manejarlo devolviendo 0:
        # self.assertEqual(escalera(-1), 0)
        pass

if __name__ == '__main__':
    unittest.main()