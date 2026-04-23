# Implementar, por división y conquista, una función que dado un arreglo sin elementos repetidos y casi ordenado (todos los elementos se encuentran ordenados, salvo uno), obtenga el elemento fuera de lugar. Indicar y justificar la complejidad.
"""
INICIO = 0
FIN = 1
DESORDENADO = 2

# Complejidad: O(n log n)
# Por Teorema Maestro, divido el problema a la mitad A = 2, llamo para ambas mitades B = 2, recorro el arreglo C = 1
def elemento_desordenado(arr):
    desordenado = elemento_desordenado_dc(arr, 0, len(arr) - 1)[DESORDENADO]
    if not desordenado:
        return arr[0] # Si no se puede determinar, por ejemplo [2,1] o [1,3,2], asumo que el primero, 2 y 3 respectivamente
    return desordenado
    
def elemento_desordenado_dc(arr, inicio, fin):
    if inicio == fin:
        return (inicio, fin, None)
    else:
        centro = (inicio + fin) // 2
        (inicio_izq, fin_izq, desordenado_izq) = elemento_desordenado_dc(arr, inicio, centro)
        (inicio_der, fin_der, desordenado_der) = elemento_desordenado_dc(arr, centro + 1, fin)

        if (desordenado_izq):
            return (None, None, desordenado_izq)
        elif (desordenado_der):
            return (None, None, desordenado_der)

        index_izq = inicio_izq
        index_der = inicio_der

        while index_izq <= fin_izq or index_der <= fin_der:
            if not index_izq <= fin_izq:
                index_der += 1
            elif not index_der <= fin_der:
                index_izq += 1
            elif arr[index_izq] < arr[index_der]:
               index_izq += 1
            else:
                if index_izq - 1 >= 0:
                    if arr[index_der] < arr[index_izq - 1]:
                        return (None, None, arr[index_der])
                    else:
                        return (None, None, arr[index_izq])
                elif index_der + 1 <= fin_der:
                    if arr[index_izq] > arr[index_der + 1]:
                        return (None, None, arr[index_izq])
                    else:
                        return (None, None, arr[index_der])
                else:
                    return (inicio_izq, fin_der, None) # Esta desordenado, pero cual?
        
        return (inicio_izq, fin_der, None)
"""

DESORDENADO = 2

def elemento_desordenado(arr):
    return elemento_desordenado_dc(arr, 0, len(arr) - 1)[DESORDENADO]

# Complejidad: O(1), No recorre el array
# Teorema Maestro, A = 2, B = 2, C = 0
# Log2(2) = 1 > 0 => n ^ log2(2) = n
def elemento_desordenado_dc(arr, inicio, fin):
    if fin - inicio == 1:
        if arr[fin] < arr[inicio]:
            return determinar_desordenado(arr, inicio, fin)
        else:
            return (inicio, fin, None)
    elif inicio == fin:
        return (inicio, fin, None)
    else:
        centro = (inicio + fin) // 2
        (inicio_izq, fin_izq, desordenado_izq) = elemento_desordenado_dc(arr, inicio, centro)
        (inicio_der, fin_der, desordenado_der) = elemento_desordenado_dc(arr, centro + 1, fin)

        if (desordenado_izq):
            return (None, None, desordenado_izq)
        elif (desordenado_der):
            return (None, None, desordenado_der)
        elif arr[inicio_der] < arr[fin_izq]:
            return determinar_desordenado(arr, fin_izq, inicio_der)
        else:
            return (inicio_izq, fin_der, None)

# Complejidad: O(1), No recorre el array
def determinar_desordenado(arr, index_izq, index_der):
    if index_izq - 1 >= 0:
        if arr[index_der] < arr[index_izq - 1]:
            return (None, None, arr[index_der])
        else:
            return (None, None, arr[index_izq])
    elif index_der + 1 <= len(arr) - 1:
        if arr[index_izq] > arr[index_der + 1]:
            return (None, None, arr[index_izq])
        else:
            return (None, None, arr[index_der])
    else:
        return (None, None, arr[index_izq])


assert elemento_desordenado([2,1]) == 2
assert elemento_desordenado([1,3,2]) == 3

assert elemento_desordenado([1,4,2,3,5]) == 4
assert elemento_desordenado([1,2,3,7,4,5,6,8]) == 7

# Caso 1: Elemento mayor movido a la derecha
assert elemento_desordenado([1, 2, 10, 3, 4, 5]) == 10

# Caso 2: Elemento menor movido a la izquierda
assert elemento_desordenado([1, 7, 2, 3, 4, 5]) == 7

# Caso 3: El elemento fuera de lugar está al principio
assert elemento_desordenado([20, 1, 2, 3, 4]) == 20

# Caso 4: El elemento fuera de lugar está al final
assert elemento_desordenado([2, 3, 4, 5, 1]) == 1
    
# Caso 5: El elemento es mucho más pequeño y está en medio
assert elemento_desordenado([10, 20, 30, 5, 40, 50]) == 5

# Caso 6: El elemento es mucho más grande y está en medio
assert elemento_desordenado([10, 20, 100, 30, 40, 50]) == 100