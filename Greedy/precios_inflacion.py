

# Complejidad: O(n log n)

# ¿El algoritmo implementado encuentra siempre la solución óptima?
# Supongamos que A es mi orden de compra óptimo y B = (b_1, ..., b_j, b_k, ..., b_n) un orden que tiene un par de elementos j, k,
# tal que j va antes que k, pero R[k] > R[j]. Entonces, el precio por ambos productos a partir de un día n, será:
# R[j]^{n + 1} + R[k]^{(n + 1) + 1}
# si intercambiamos estos elementos el precio será:
# R[k]^{n + 1} + R[j]^{(n + 1) + 1}
# y (R[k]^{n + 1} + R[j]^{(n + 1) + 1}) <= (R[j]^{n + 1} + R[k]^{(n + 1) + 1}), ya que R[j] < R[k], es decir un precio total mejor
# es decir que intercambiar cualquiera de los elementos no ordenado nos da una solución mejor, probando que si todos están ordenados es la solución óptima

# ¿Por qué se trata de un algoritmo Greedy?
# Porque siempre elige un maximo local para llegar a un maximo global,
# en este caso, siempre elige comprar el producto más caro primero, esto minimiza el efecto de la inflacion
# ya que los productos afectados serán los más baratos, minimizando el precio total
def precios_inflacion(R):
    R.sort(reverse=True) # O(n log n)
    precio_minimo = 0
    for dia in range(len(R)): # O(n)
        precio_minimo += R[dia] ** (dia + 1)
    return precio_minimo


def test_precios_inflacion():
    casos = [
        {"input": [2, 5], "expected": 9},
        {"input": [10, 2, 3], "expected": 27},
        {"input": [4, 4, 4], "expected": 84},
        {"input": [1, 5, 2], "expected": 10},
        {"input": [7], "expected": 7},
        {"input": [10, 20], "expected": 120}
    ]

    for i, caso in enumerate(casos):
        resultado = precios_inflacion(caso["input"])
        if resultado == caso["expected"]:
            print(f"Test {i + 1}: PASSED ✅")
        else:
            print(f"Test {i + 1}: FAILED ❌ (Esperaba {caso['expected']}, obtuve {resultado})")


if __name__ == '__main__':
    test_precios_inflacion()