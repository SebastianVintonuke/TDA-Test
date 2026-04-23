"""
def indice_mas_bajo(alumnos):
    return indice_mas_bajo_recursivo(alumnos, 0, len(alumnos) - 1)

def indice_mas_bajo_recursivo(alumnos, inicio, fin):
    if (fin - inicio == 0):
        return inicio
    else:
        centro = (inicio + fin) // 2
        izquierda = indice_mas_bajo_recursivo(alumnos, inicio, centro)
        derecha = indice_mas_bajo_recursivo(alumnos, centro + 1, fin)
        return izquierda if (alumnos[izquierda]["altura"] < alumnos[derecha]["altura"]) else derecha
"""

class Alumno:
    def __init__(self, nombre, altura):
        self.nombre = nombre
        self.altura = altura

alumnos = [
    Alumno("A", 1.2),
    Alumno("B", 1.15),
    Alumno("C", 1.14),
    Alumno("D", 1.12),
    Alumno("E", 1.02),
    Alumno("F", 0.98),
    Alumno("G", 1.18),
    Alumno("H", 1.23)
]

def indice_mas_bajo(alumnos):
    return indice_mas_bajo_recursivo(alumnos, 0, len(alumnos) - 1)

def indice_mas_bajo_recursivo(alumnos, inicio, fin):
    if (fin - inicio == 0):
        return inicio
    elif (fin - inicio == 1):
        return inicio if (alumnos[inicio].altura < alumnos[fin].altura) else fin
    else:
        centro = (inicio + fin) // 2
        siguiente = centro + 1

        if (alumnos[centro].altura < alumnos[siguiente].altura):
            return indice_mas_bajo_recursivo(alumnos, inicio, centro)
        else:
            return indice_mas_bajo_recursivo(alumnos, siguiente, fin)

def validar_mas_bajo(alumnos, indice):
    if (len(alumnos) == 1):
        return True
    elif (indice == 0):
        return alumnos[indice].altura < alumnos[indice + 1].altura
    elif (indice == len(alumnos) - 1):
        return alumnos[indice - 1].altura > alumnos[indice].altura
    else:
        return alumnos[indice - 1].altura > alumnos[indice].altura < alumnos[indice + 1].altura

indice = indice_mas_bajo(alumnos)
print(f"el indice mas bajo es: {indice}, y el alumno es: {alumnos[indice].nombre}, es correcto: {validar_mas_bajo(alumnos, indice)}")