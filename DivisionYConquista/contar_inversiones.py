from collections import deque
from itertools import islice


# Complejidad: O(n log(n)) por ordenar_y_contar
def contar_inversiones(A, B):
    if len(A) == 0 or len(A) == 1 or len(B) == 0 or len(B) == 1:
        return 0

    posiciones = dict()
    for i, a in enumerate(A):
        posiciones[a] = i

    posiciones_desordenadas = deque()
    for b in B:
        posiciones_desordenadas.append(posiciones[b])

    _, inversiones = ordenar_y_contar(posiciones_desordenadas)
    return inversiones


# Teorema Maestro, A = 2, B = 2, C = 1
# Log_2(2) = 1 = C => n ^ C log_B(n) = n log(n)
def ordenar_y_contar(L):
    if len(L) == 1:
        return L, 0
    if len(L) == 2:
        if L[0] < L[1]:
            return L, 0
        else:
            return deque([L[1], L[0]]), 1

    else:
        centro = len(L) // 2
        izq = deque(islice(L, centro))
        der = deque(islice(L, centro, len(L)))

        (union_izq, inversiones_izq) = ordenar_y_contar(izq)
        (union_der, inversiones_der) = ordenar_y_contar(der)

        union, inversiones_union = unir_y_contar(union_izq, union_der)
        inversiones = inversiones_izq + inversiones_der + inversiones_union

        return union, inversiones

# Complejidad: O(n) recorre ambos array una vez
def unir_y_contar(A, B):
    union = deque()
    numero_de_inversiones = 0

    while A and B:
        if A[0] <= B[0]:
            union.append(A.popleft())
        else:
            union.append(B.popleft())
            numero_de_inversiones += len(A)

    if A:
        union.extend(A)
    elif B:
        union.extend(B)

    return union, numero_de_inversiones



import unittest
class TestInversiones(unittest.TestCase):

    def test_ya_ordenado(self):
        # Si B ya es igual a A, hay 0 inversiones
        A = [1, 2, 3, 4, 5]
        B = [1, 2, 3, 4, 5]
        self.assertEqual(contar_inversiones(A, B), 0)

    def test_totalmente_invertido(self):
        # Si B es el reverso de A, las inversiones son n*(n-1)/2
        # Para n=4: 4*3 / 2 = 6
        A = ['a', 'b', 'c', 'd']
        B = ['d', 'c', 'b', 'a']
        self.assertEqual(contar_inversiones(A, B), 6)

    def test_un_solo_cambio(self):
        # Solo un par intercambiado (el 2 y el 3)
        A = [10, 20, 30, 40]
        B = [10, 30, 20, 40]
        self.assertEqual(contar_inversiones(A, B), 1)

    def test_elementos_no_numericos(self):
        # El arreglo A define que "manzana" < "pera" < "uva"
        A = ["manzana", "pera", "uva"]
        B = ["uva", "manzana", "pera"]
        # "uva" genera 2 inversiones: (uva, manzana) y (uva, pera)
        self.assertEqual(contar_inversiones(A, B), 2)

    def test_caso_vacio_y_unitario(self):
        self.assertEqual(contar_inversiones([], []), 0)
        self.assertEqual(contar_inversiones([1], [1]), 0)

    def test_aleatorio_mixto(self):
        A = [1, 2, 3, 4, 5, 6]
        B = [1, 5, 2, 4, 3, 6]
        # Inversiones: (5,2), (5,4), (5,3), (2, no), (4,3) -> Total: 4
        self.assertEqual(contar_inversiones(A, B), 4)

if __name__ == '__main__':
    unittest.main()