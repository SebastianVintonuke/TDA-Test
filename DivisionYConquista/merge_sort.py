"""
def merge_sort(arr):
    return merge_sort_dc(arr, 0, len(arr) - 1)

# Complejidad: O(n log(n))
# Teorema Maestro, A = 2, B = 2, C = 1
# Log2(2) = 1 = C => n ^ 1 * log2(n) = n log(n)
def merge_sort_dc(arr, inicio, fin):
    if fin - inicio == 0:
        return [arr[inicio]]
    else:
        centro = (inicio + fin) // 2
        izq = merge_sort_dc(arr, inicio, centro)
        der = merge_sort_dc(arr, centro + 1, fin)
        return juntar(izq, der)

# Complejidad: O(n)
def juntar(izq, der):
    resultado = []
    while izq or der:
        if not izq:
            resultado.append(der.pop(0))
        elif not der:
            resultado.append(izq.pop(0))
        elif izq[0] < der[0]:
            resultado.append(izq.pop(0))
        else:
            resultado.append(der.pop(0))
    return resultado
"""

def merge_sort(arr):
    if not arr:
        return arr
    return merge_sort_dc(arr, 0, len(arr) - 1)

# Complejidad: O(n log(n))
# Teorema Maestro, A = 2, B = 2, C = 1
# Log2(2) = 1 = C => n ^ 1 * log2(n) = n log(n)
def merge_sort_dc(arr, inicio, fin):
    if fin - inicio == 0:
        return [arr[inicio]]
    else:
        centro = (inicio + fin) // 2
        izq = merge_sort_dc(arr, inicio, centro)
        der = merge_sort_dc(arr, centro + 1, fin)
        return juntar(izq, der)

# Complejidad: O(n)
def juntar(izq, der):
    resultado = []
    indice_izq = 0
    indice_der = 0
    while indice_izq < len(izq) or indice_der < len(der):
        if indice_izq == len(izq):
            resto = der[indice_der:]
            resultado.extend(resto)
            indice_der += len(resto)
        elif indice_der == len(der):
            resto = izq[indice_izq:]
            resultado.extend(resto)
            indice_izq += len(resto)
        elif izq[indice_izq] < der[indice_der]:
            resultado.append(izq[indice_izq])
            indice_izq += 1
        else:
            resultado.append(der[indice_der])
            indice_der += 1
    return resultado

print(merge_sort([3,0,-1,2,6,-7,10,100,2,-1,3]))