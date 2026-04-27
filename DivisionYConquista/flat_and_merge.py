def flat_and_merge(arreglos):
    return flat_and_merge_rec(arreglos, 0, len(arreglos))

def flat_and_merge_rec(arreglos, inicio, fin):
    cantidad_de_elementos = fin - inicio
    if cantidad_de_elementos == 1:
        return arreglos[inicio]
    else:
        centro = inicio + (fin - inicio) // 2
        izq = flat_and_merge_rec(arreglos, inicio, centro)
        der = flat_and_merge_rec(arreglos, centro, fin)

        return merge(izq, der)

def merge(arr1, arr2):
    resultado = []
    h1 = 0
    h2 = 0
    while h1 <= len(arr1) and h2 <= len(arr2):
        if h1 == len(arr1):
            resultado.append(arr2[h2])
            h2 += 1
        elif h2 == len(arr2):
            resultado.append(arr1[h1])
            h1 += 1
        elif arr1[h1] >= arr2[h2]:
            resultado.append(arr1[h1])
            h1 += 1
        else:
            resultado.append(arr2[h2])
            h2 += 1
    return resultado