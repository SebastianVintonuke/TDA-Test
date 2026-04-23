INICIO = 0
FIN = 1
SUMATORIA= 2

def max_subarray(arr):
    (inicio, fin, _) = max_subarray_dc(arr, 0, len(arr) - 1)
    return arr[inicio:fin + 1]

# Complejidad O(n log n)
# Parte el problema al medio (A = 2), para cada mitad (B = 2) llama a "max_desde_hasta" (O(n)) (C = 1)
#
# Teorema Maestro T(n) = AT(n/B) + O(n^C)
#              < -> T(n) = O(n^C)
# Si LogB(A) = C -> T(n) = O(n^C logB(n)) = O(n^C log(n))
#              > -> T(n) = O(n^logB(A))
#
# T(n) = 2T (n/2) + 0(n^1) => log2(2) = 1 = C => O(n log n)
def max_subarray_dc(arr, inicio, fin):
    if inicio == fin:
        return (inicio, fin, arr[inicio])
    else:
        centro = (inicio + fin) // 2
        max_subarray_izq = max_subarray_dc(arr, inicio, centro)
        max_subarray_der = max_subarray_dc(arr, centro + 1, fin)

        centro_entre_lados = (max_subarray_izq[INICIO] + max_subarray_der[FIN]) // 2
        (inicio_max_sumatoria_entre_lados, max_sumatoria_centro_a_izq) = max_desde_hasta(arr, centro_entre_lados, max_subarray_izq[INICIO], -1)
        (fin_max_sumatoria_entre_lados, max_sumatoria_centro_a_der) = max_desde_hasta(arr, centro_entre_lados + 1, max_subarray_der[FIN], 1)
        
        max_subarray_lado = max_subarray_izq if max_subarray_izq[SUMATORIA] > max_subarray_der[SUMATORIA] else max_subarray_der
        max_subarray_centro = (inicio_max_sumatoria_entre_lados, fin_max_sumatoria_entre_lados, max_sumatoria_centro_a_izq + max_sumatoria_centro_a_der)

        return max_subarray_centro if (max_subarray_centro[SUMATORIA] > max_subarray_lado[SUMATORIA]) else max_subarray_lado

# Complejidad O(n)
# Itera arr[inicio:fin]
def max_desde_hasta(arr, inicio, fin, paso):
    sumatoria = arr[inicio]
    max_sumatoria = arr[inicio]
    indice_max_sumatoria = inicio
    for indice in range(inicio + paso, fin + paso, paso):
        sumatoria += arr[indice]
        if sumatoria > max_sumatoria:
            max_sumatoria = sumatoria
            indice_max_sumatoria = indice
    return (indice_max_sumatoria, max_sumatoria)

#assert max_subarray([5, 3, 2, 4, -1]) == [5, 3, 2, 4]
#assert max_subarray([5, 3, -5, 4, -1]) == [5, 3]
#assert max_subarray([5, -4, 2, 4, -1]) == [5, -4, 2, 4]
#assert max_subarray([5, -4, 2, 4]) == [5, -4, 2, 4]
#assert max_subarray([-3, 4, -1, 2, 1, -5]) == [4, -1, 2, 1]
#assert max_subarray([-3, -4, -1, 0, -2, -1, -5]) == [0]

print(max_subarray([1,-1,0,1,-1,0,1,-1]))
assert max_subarray([1,-1,0,1,-1,0,1,-1]) == [1,-1,0,1,-1,0,1]