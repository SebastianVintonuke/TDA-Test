
def indice_primer_cero(arr):
    if not arr or arr[len(arr) - 1] == 1:
        return -1
    elif arr[0] == 0:
        return 0
    return indice_primer_cero_dc(arr, 0, len(arr))

# Complejidad: O(log(n)
# Teorema Maestro, A = 1, B = 2, C = 0
# Log2(2) = 1 > 0 => n ^ 0 * log2(n) = log(n)
def indice_primer_cero_dc(arr, inicio, fin):
    if inicio == fin:
        return -1
    elif el_array_tiene_dos_elementos(inicio, fin) and son_el_punto_de_transicion(arr, inicio, fin):
        return fin
    else:
        centro = (inicio + fin) // 2

        if arr[centro] == 0:
            return indice_primer_cero_dc(arr, inicio, centro)
        else:
            return indice_primer_cero_dc(arr, centro, fin)

# Complejidad: O(1)
def el_array_tiene_dos_elementos(inicio, fin):
    return fin - inicio == 1

# Complejidad: O(1)
def son_el_punto_de_transicion(arr, inicio, fin):
    return arr[inicio] == 1 and arr[fin] == 0

assert indice_primer_cero([1, 1, 0]) == 2

# Casos normales (el cero está en el medio)
assert indice_primer_cero([1, 1, 1, 0, 0]) == 3
assert indice_primer_cero([1, 1, 0, 0, 0, 0]) == 2
assert indice_primer_cero([1, 0, 0, 0, 0]) == 1

# Casos borde: el cero está en la primera posición (todos ceros)
assert indice_primer_cero([0, 0, 0, 0, 0]) == 0
assert indice_primer_cero([0]) == 0

# Casos borde: no hay ningún cero (todos unos)
assert indice_primer_cero([1, 1, 1, 1, 1]) == -1
assert indice_primer_cero([1]) == -1

# Casos de arreglos pequeños (tamaño 2)
assert indice_primer_cero([1, 0]) == 1
assert indice_primer_cero([1, 1]) == -1
assert indice_primer_cero([0, 0]) == 0

# Caso borde: arreglo vacío (si el enunciado lo permite, no hay 0)
assert indice_primer_cero([]) == -1

# Pruebas de volumen (ideales para comprobar que tu solución es O(log n) y no O(n))
assert indice_primer_cero([1] * 500000 + [0] * 500000) == 500000
assert indice_primer_cero([1] * 1000000) == -1
assert indice_primer_cero([0] * 1000000) == 0
assert indice_primer_cero([1] * 999999 + [0]) == 999999
