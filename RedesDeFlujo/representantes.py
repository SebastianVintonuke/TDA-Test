from RedesDeFlujo.grafo import Grafo
from collections import deque


# C: numero de clubes
# P: numero de partidos politicos
# M: numero de miembros
# La complejidad va está acotada por la función flujo la cual tiene complejidad O(V*E^2)
# con: V = C + P + M
# y: E =    P    +   M    +  P*C   +   C
#        (Fu->P)   (P->M)   (M->C)   (C->Su)
# siendo P*C el peor caso donde todos los miembros están afiliados a todos los clubes
def representantes(miembros):
    clubes = set()
    partidos_politicos = set()
    for miembro in miembros: # O(M)
        partidos_politicos.add(miembro.partido_politico)
        for club in miembro.clubes: # O(M+C)
            clubes.add(club)
    n = len(clubes)

    red_de_flujo = Grafo(True, list(clubes) + list(partidos_politicos) + list(map(lambda m: m.nombre, miembros)))

    red_de_flujo.agregar_vertice("Fuente")
    red_de_flujo.agregar_vertice("Sumidero")

    for partido_politico in partidos_politicos:
        red_de_flujo.agregar_arista("Fuente", partido_politico, n//2) # Para que cada club solo tengo un representante
    for club in clubes:
        red_de_flujo.agregar_arista(club, "Sumidero", 1) # Para que cada club solo tenga un miembro asignado
    for miembro in miembros:
        red_de_flujo.agregar_arista(miembro.partido_politico, miembro.nombre, 1) # Asocia al miembro con su partido político
        for club in miembro.clubes:
            red_de_flujo.agregar_arista(miembro.nombre, club, 1) # El miembro debe pertenecer al club para representarlo

    flujos = flujo(red_de_flujo, "Fuente", "Sumidero")

    asignaciones = [arista for arista, peso in flujos.items() if arista[1] in clubes and peso == 1]

    if len(asignaciones) < n:
        return None

    resultado = {}
    for asignacion in asignaciones:
        resultado[asignacion[0]] = asignacion[1]

    return resultado




























def flujo(grafo, s, t):
    asignacion = {}
    for v in grafo:
        for w in grafo.adyacentes(v):
            asignacion[(v, w)] = 0
    grafo_residual = copiar(grafo)
    camino = obtener_camino(grafo_residual, s, t)
    while camino is not None:
        capacidad_residual_camino = min_peso(grafo_residual, camino)
        for i in range(1, len(camino)):
            if grafo.estan_unidos(camino[i-1], camino[i]):
                asignacion[(camino[i-1], camino[i])] += capacidad_residual_camino
            else:
                asignacion[(camino[i], camino[i-1])] -= capacidad_residual_camino
            actualizar_grafo_residual(grafo_residual, camino[i-1], camino[i], capacidad_residual_camino)
        camino = obtener_camino(grafo_residual, s, t)
    return asignacion

def actualizar_grafo_residual(grafo_residual, u, v, valor):
    peso_anterior = grafo_residual.peso_arista(u, v)
    if peso_anterior == valor:
        grafo_residual.borrar_arista(u, v)
    else:
        grafo_residual.cambiar_peso(u, v, peso_anterior - valor)
    if not grafo_residual.estan_unidos(v, u):
        grafo_residual.agregar_arista(v, u, valor)
    else:
        grafo_residual.cambiar_peso(v, u, grafo_residual.peso_arista(v, u) + valor)

def copiar(g):
    nuevo = Grafo(True, g.obtener_vertices())
    for v in g:
        for w in g.adyacentes(v):
            nuevo.agregar_arista(v, w, g.peso_arista(v, w))
    return nuevo

def obtener_camino(g, org, dst):
    padre = {org: None}
    cola = deque()
    cola.append(org)
    while len(cola) > 0:
        v = cola.popleft()
        if v == dst:
            camino = []
            while v is not None:
                camino.append(v)
                v = padre[v]
            return camino[::-1]
        for w in g.adyacentes(v):
            if w not in padre:
                padre[w] = v
                cola.append(w)
    return None

def min_peso(grafo, camino):
    cap = grafo.peso_arista(camino[0], camino[1])
    for i in range(1, len(camino) - 1):
        cap = min(cap, grafo.peso_arista(camino[i], camino[i+1]))
    return cap


import unittest
import os


class TestRepresentantesComision(unittest.TestCase):

    def validar_asignacion(self, miembros, resultado, clubes_esperados):
        """
        Función auxiliar para validar exhaustivamente las reglas del problema.
        """
        # 1. Verificar que devolvió un resultado y no None
        self.assertIsNotNone(resultado, "El algoritmo devolvió None, pero se esperaba una solución válida.")

        # 2. Verificar que todos los clubes están representados exactamente una vez
        clubes_asignados = list(resultado.values())
        self.assertEqual(len(clubes_asignados), len(clubes_esperados),
                         "La cantidad de clubes asignados no coincide con la cantidad total de clubes.")
        self.assertCountEqual(clubes_asignados, clubes_esperados,
                              "No todos los clubes fueron representados o hay clubes inexistentes.")

        # 3. Verificar que un representante no esté asignado a más de un club
        representantes_asignados = list(resultado.keys())
        self.assertEqual(len(representantes_asignados), len(set(representantes_asignados)),
                         "Una persona está representando a más de un club.")

        diccionario_miembros = {m["nombre"]: m for m in miembros}
        conteo_partidos = {}

        for representante, club in resultado.items():
            # 4. Verificar que el representante exista en la lista original
            self.assertIn(representante, diccionario_miembros, f"El representante '{representante}' no existe.")

            # 5. Verificar que el representante realmente pertenezca al club que representa
            clubes_del_representante = diccionario_miembros[representante]["clubes"]
            self.assertIn(club, clubes_del_representante,
                          f"El representante '{representante}' no pertenece al '{club}'.")

            # Registrar partido para la validación final
            partido = diccionario_miembros[representante]["partido_politico"]
            conteo_partidos[partido] = conteo_partidos.get(partido, 0) + 1

        # 6. Verificar restricción de partido político (máximo n/2)
        n = len(clubes_esperados)
        limite_partido = n // 2
        for partido, cantidad in conteo_partidos.items():
            self.assertLessEqual(cantidad, limite_partido,
                                 f"El partido '{partido}' tiene {cantidad} representantes, superando el límite de {limite_partido} (n/2 donde n={n}).")

    # ==========================================
    # TESTS BÁSICOS
    # ==========================================

    def test_caso_basico_exitoso(self):
        miembros = [
            {"nombre": "A", "clubes": ["Club1"], "partido_politico": "P1"},
            {"nombre": "B", "clubes": ["Club2"], "partido_politico": "P2"},
            {"nombre": "C", "clubes": ["Club3"], "partido_politico": "P3"},
            {"nombre": "D", "clubes": ["Club1", "Club4"], "partido_politico": "P1"}
        ]
        clubes_esperados = ["Club1", "Club2", "Club3", "Club4"]
        resultado = representantes(miembros)
        self.validar_asignacion(miembros, resultado, clubes_esperados)

    def test_sin_solucion_por_exceso_partido(self):
        # 4 clubes, límite n/2 = 2. Aquí P1 obligatoriamente tendrá 3 representantes.
        miembros = [
            {"nombre": "A", "clubes": ["Club1"], "partido_politico": "P1"},
            {"nombre": "B", "clubes": ["Club2"], "partido_politico": "P1"},
            {"nombre": "C", "clubes": ["Club3"], "partido_politico": "P1"},
            {"nombre": "D", "clubes": ["Club4"], "partido_politico": "P2"}
        ]
        resultado = representantes(miembros)
        self.assertIsNone(resultado, "Debería devolver None porque el partido P1 supera el límite de n/2.")

    def test_sin_solucion_por_falta_de_representantes(self):
        # 3 clubes, pero solo 2 personas en total en el pueblo. Imposible cumplir "1 persona = 1 club".
        miembros = [
            {"nombre": "A", "clubes": ["Club1", "Club2"], "partido_politico": "P1"},
            {"nombre": "B", "clubes": ["Club2", "Club3"], "partido_politico": "P2"}
        ]
        resultado = representantes(miembros)
        self.assertIsNone(resultado,
                          "Debería devolver None porque no hay suficientes personas para representar a todos los clubes distintos.")

    def test_multiples_clubes_resolucion_compleja(self):
        # A puede ir al C1 o C2, B puede ir al C2 o C3, C puede ir al C3 o C1.
        miembros = [
            {"nombre": "A", "clubes": ["C1", "C2"], "partido_politico": "P1"},
            {"nombre": "B", "clubes": ["C2", "C3"], "partido_politico": "P2"},
            {"nombre": "C", "clubes": ["C3", "C1"], "partido_politico": "P3"}
        ]
        clubes_esperados = ["C1", "C2", "C3"]
        resultado = representantes(miembros)
        self.validar_asignacion(miembros, resultado, clubes_esperados)

    # ==========================================
    # TEST DE VOLUMEN
    # ==========================================

    def test_volumen_archivo_adjunto(self):
        """
        Lee el archivo de volumen, lo parsea y verifica la correcta ejecución
        del algoritmo de flujo máximo.
        """
        archivo_volumen = 'volumen.txt'

        # Saltar la prueba si el archivo no existe en el entorno de test
        if not os.path.exists(archivo_volumen):
            self.skipTest(f"El archivo {archivo_volumen} no se encuentra en el directorio.")

        miembros = []
        clubes_esperados = set()

        # Parsear el archivo con el formato: id,partido,club_A,club_B
        with open(archivo_volumen, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(',')
                nombre = partes[0]
                partido = partes[1]
                clubes = partes[2:]  # Los clubes son todos los elementos desde el índice 2 en adelante

                miembros.append({
                    "nombre": nombre,
                    "clubes": clubes,
                    "partido_politico": partido
                })

                for c in clubes:
                    clubes_esperados.add(c)

        clubes_esperados = list(clubes_esperados)

        # Ejecutar el algoritmo
        resultado = representantes(miembros)

        # Validar exhaustivamente
        self.validar_asignacion(miembros, resultado, clubes_esperados)


if __name__ == '__main__':
    unittest.main()

