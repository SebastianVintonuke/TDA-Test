
# Complejidad: O(log(n))
# Teorema Maestro, A = 1, B = 2, C = 0
# Log2(1) = 0 = C => n ^ 0 * log2(n) = log(n)
def posicion_pico(v, ini, fin):
    centro = (ini + fin) // 2
    siguiente = centro + 1
    anterior = centro - 1

    if es_el_punto_de_quiebre(v, anterior, centro, siguiente):
        return centro
    elif esta_creciendo(v, anterior, centro, siguiente):
        return posicion_pico(v, centro, fin)
    else:
        return posicion_pico(v, ini, centro)


# Complejidad: O(1)
def esta_creciendo(arr, anterior, actual, siguiente):
    return arr[anterior] < arr[actual] < arr[siguiente]

# Complejidad: O(1)
def es_el_punto_de_quiebre(arr, anterior, actual, siguiente):
    return arr[anterior] < arr[actual] > arr[siguiente]













array = [1, 2, 3, 1, 0, -2]
#assert posicion_pico(array, 0, len(array)-1) == 2


def test_posicion_pico():
    # Caso del enunciado
    assert posicion_pico([1, 2, 3, 1, 0, -2], 0, 5) == 2

    # Pico mínimo (N=3)
    assert posicion_pico([1, 10, 2], 0, 2) == 1

    # Pico hacia el final
    assert posicion_pico([1, 2, 3, 4, 5, 2], 0, 5) == 4

    # Pico hacia el principio
    assert posicion_pico([1, 5, 4, 3, 2, 1], 0, 5) == 1

    # Pico con números negativos
    assert posicion_pico([-10, -5, 0, 5, -2, -15], 0, 5) == 3

    # Pico en arreglo de tamaño impar
    assert posicion_pico([0, 2, 4, 6, 4, 2, 0], 0, 6) == 3

    # Pico en arreglo de tamaño par
    assert posicion_pico([10, 20, 30, 40, 50, 45], 0, 5) == 4

    # Secuencia larga
    larga = list(range(100)) + list(range(98, -1, -1))
    assert posicion_pico(larga, 0, len(larga) - 1) == 99

    print("✅ ¡Todos los asserts pasaron exitosamente!")

# Para ejecutar las pruebas:
test_posicion_pico()