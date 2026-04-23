# Complejidad: O(n log n)

# ¿El algoritmo implementado encuentra siempre la solución óptima?
# Supongamos que A es mi orden de compra óptimo y B = (b_1, ..., b_j, b_k, ..., b_n) un orden que tiene un par de elementos j, k,
# tal que j va antes que k, pero R[k] < R[j]. Entonces, el precio por ambos productos a partir de un día n, será:
# R[j] / 2^n + R[k] / 2^(n + 1)
# si intercambiamos estos elementos el precio será:
# R[k] / 2^n + R[j] / 2^(n + 1)
# y R[k] / 2^n + R[j] / 2^(n + 1) <= R[j] / 2^n + R[k] / 2^(n + 1), ya que R[j] > R[k], es decir un precio total mejor, ya que el denominador en días posteriores será más grande
# es decir que intercambiar cualquiera de los elementos no ordenado nos da una solución mejor, probando que si todos están ordenados es la solución óptima

# ¿Por qué se trata de un algoritmo Greedy?
# Porque siempre elige un maximo local para llegar a un maximo global,
# en este caso, siempre elige comprar el producto más barato primero, esto maximiza el efecto de la deflacion
# ya que los productos afectados serán los más caros, minimizando el precio total
def precios_deflacion(R):
    R.sort()  # O(n log n)
    precio_minimo = 0
    for dia in range(len(R)):  # O(n)
            precio_minimo += R[dia] / (2 ** dia)
    return precio_minimo












def test_precios_deflacion():
    casos = [
        {"input": [10, 100], "expected": 60.0},
        {"input": [40, 20, 80], "expected": 60.0},
        {"input": [16, 16, 16], "expected": 28.0},
        {"input": [1, 2, 4, 8], "expected": 4.0},
        {"input": [5, 5], "expected": 7.5},
        {"input": [50], "expected": 50.0}
    ]

    for i, caso in enumerate(casos):
        resultado = precios_deflacion(caso["input"])
        # Usamos round o un margen de error pequeño por tratarse de floats
        if abs(resultado - caso["expected"]) < 1e-9:
            print(f"Test {i + 1}: PASSED ✅")
        else:
            print(f"Test {i + 1}: FAILED ❌ (Esperaba {caso['expected']}, obtuve {resultado})")

if __name__ == '__main__':
    test_precios_deflacion()