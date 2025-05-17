import time 
from django.db import connection, transaction
from .models import GrupoRLCP, LimeSurvey583965, ConceptosGruposRLCP
from itertools import combinations
import concurrent.futures 
from django.db import close_old_connections
from itertools import product

VALORES_MAPEO = {'Bajo': 0, 'Medio': 1, 'Alto': 2}
VALORES_INVERSO = {0: 'Bajo', 1: 'Medio', 2: 'Alto'}

CAMPOS_COMPARABLES = [
    'number_583965x21x436sq001', 'number_583965x21x436sq002', 'number_583965x21x436sq003',
    'number_583965x21x436sq004', 'number_583965x21x436sq005', 'number_583965x21x436sq006',
    'number_583965x21x436sq007', 'number_583965x21x436sq008', 'number_583965x21x436sq009',
    'number_583965x21x436sq010', 'number_583965x21x436sq011', 'number_583965x21x436sq012',
    'number_583965x21x436sq013', 'number_583965x21x436sq014', 'number_583965x21x436sq015',
    'number_583965x21x436sq016', 'number_583965x21x436sq017', 'number_583965x21x436sq018',
    'number_583965x21x436sq019', 'number_583965x21x436sq020', 'number_583965x21x436sq021',
    'number_583965x21x436sq022', 'number_583965x21x436sq023', 'number_583965x21x436sq024',
    'number_583965x21x436sq025', 'number_583965x21x436sq026', 'number_583965x21x436sq027',
    'number_583965x21x436sq028', 'number_583965x21x436sq029', 'number_583965x21x436sq030',
    'number_583965x21x436sq031', 'number_583965x21x436sq032'
]

MAX_ATRIBUTOS = 20
MAX_TESTORES_POR_TAMAÑO = 15

def obtener_respuestas_grupo(grupo: GrupoRLCP):
    ids = grupo.ids_respuestas.split(',')
    respuestas = list(
        LimeSurvey583965.objects.filter(id__in=ids)
        .values_list(*CAMPOS_COMPARABLES[:MAX_ATRIBUTOS])
    )
    respuestas_numericas = []
    for fila in respuestas:
        convertida = []
        for valor in fila:
            if valor in VALORES_MAPEO:
                convertida.append(VALORES_MAPEO[valor])
            else:
                convertida.append(None)
        if all(v is not None for v in convertida):
            respuestas_numericas.append(convertida)
    return respuestas_numericas

def construir_matriz_diferencia(respuestas):
    matriz = []
    n = len(respuestas)
    for i in range(n):
        for j in range(i + 1, n):
            fila_diff = [1 if respuestas[i][k] != respuestas[j][k] else 0 for k in range(MAX_ATRIBUTOS)]
            if any(fila_diff):
                matriz.append(fila_diff)
    return matriz

def es_testor(candidatos, matriz_diff):
    for fila in matriz_diff:
        if not any(fila[i] for i in candidatos):
            return False
    return True

def extraer_testores(matriz_diff, max_longitud=5):
    testores = []
    for r in range(1, max_longitud + 1):
        encontrados = 0
        for comb in combinations(range(MAX_ATRIBUTOS), r):
            if es_testor(comb, matriz_diff):
                if not any(set(comb).issuperset(set(t)) for t in testores):
                    testores.append(comb)
                    encontrados += 1
            if encontrados >= MAX_TESTORES_POR_TAMAÑO:
                break
    return testores

def extraer_testores_relajados(matriz_diff, umbral_cobertura=0.5):
    testores = []
    total_filas = len(matriz_diff)
    min_filas = int(total_filas * umbral_cobertura)
    for r in range(1, MAX_ATRIBUTOS + 1):
        for comb in combinations(range(MAX_ATRIBUTOS), r):
            cubiertas = sum(1 for fila in matriz_diff if any(fila[i] for i in comb))
            if cubiertas >= min_filas:
                testores.append(comb)
                return testores  # Solo uno
    return []

def extraer_testores_por_frecuencia(matriz_diff, min_cobertura=0.5):
    total_filas = len(matriz_diff)
    min_filas = int(total_filas * min_cobertura)
    mejores_testores = []
    for r in range(1, 6):
        for comb in combinations(range(MAX_ATRIBUTOS), r):
            cubiertas = sum(1 for fila in matriz_diff if any(fila[i] for i in comb))
            if cubiertas >= min_filas:
                mejores_testores.append((comb, cubiertas))
        if mejores_testores:
            # Ordenamos por peso descendente (cubiertas) y luego por longitud ascendente (cardinalidad)
            mejores_testores.sort(key=lambda x: (-x[1], len(x[0])))
            return [mejores_testores[0][0]]
    return []

def calcular_peso(testor, matriz_diff):
    return sum(1 for fila in matriz_diff if any(fila[i] for i in testor))

def seleccionar_testor_mas_representativo(testores, matriz_diff):
    # Ordenamos por peso descendente, y si hay empate, por cardinalidad ascendente
    testores_info = [(calcular_peso(t, matriz_diff), len(t), t) for t in testores]
    testores_info.sort(key=lambda x: (-x[0], x[1]))
    return testores_info[0][2]

def construir_conceptos(testor, respuestas):
    """
    Construye todas las combinaciones posibles de valores reales para cada atributo del testor.
    Devuelve una lista de tuplas, donde cada tupla es una combinación válida.
    """
    valores_por_atributo = []

    for i in testor:
        valores = [fila[i] for fila in respuestas if fila[i] is not None]
        valores_unicos = sorted(set(valores))
        if valores_unicos:
            valores_por_atributo.append([VALORES_INVERSO[v] for v in valores_unicos])
        else:
            valores_por_atributo.append(["Desconocido"])

    # Generar todas las combinaciones posibles
    combinaciones = list(product(*valores_por_atributo))
    return combinaciones

def generalizar_concepto(testor, respuestas):
    reglas = []

    for i in testor:
        valores = [fila[i] for fila in respuestas if fila[i] is not None]
        if valores:
            valores_distintos = sorted(set(valores))
            valores_legibles = ','.join([VALORES_INVERSO[v] for v in valores_distintos])
            reglas.append(f"Pregunta{i+1}=({valores_legibles})")
        else:
            reglas.append(f"Pregunta{i+1}=(Desconocido)")

    resultado = '[' + '^'.join(reglas) + ']'
    return str(resultado)  # Asegura que el resultado sea tipo string plano



def guardar_conceptos(grupo_id, respuestas, testores, matriz_diff):
    testor_seleccionado = seleccionar_testor_mas_representativo(testores, matriz_diff)
    concepto = construir_conceptos(testor_seleccionado, respuestas)
    concepto_general = generalizar_concepto(testor_seleccionado, respuestas)
    recomendacion = generar_recomendacion_concepto(concepto_general)

    preguntas_legibles = [f"Pregunta {i+1}" for i in testor_seleccionado]

    with transaction.atomic():
        ConceptosGruposRLCP.objects.create(
            grupo_id=grupo_id,
            testor=','.join(preguntas_legibles),
            concepto=','.join([str(c) for c in concepto]),
            concepto_general=generalizar_concepto(testor_seleccionado, respuestas),
            recomendacion=recomendacion
        )

def guardar_concepto_sin_testores(grupo_id, respuestas, mensaje):
    with transaction.atomic():
        ConceptosGruposRLCP.objects.create(
            grupo_id=grupo_id,
            testor="No se encontró un testor",
            concepto="No se generó un concepto",
            concepto_general="No se generó un concepto general",
            recomendacion=mensaje
        )

import re

def generar_recomendacion_concepto(concepto_general):
    # Extraer todos los valores entre paréntesis (ej: 'Medio', 'Alto') usando regex
    valores_extraidos = re.findall(r'\((.*?)\)', concepto_general)
    
    # Separar los valores por coma y aplanar
    valores = []
    for grupo in valores_extraidos:
        valores.extend(grupo.split(','))

    # Limpiar espacios y mapear a números
    valores_numericos = [VALORES_MAPEO.get(valor.strip(), None) for valor in valores]
    valores_numericos = [v for v in valores_numericos if v is not None]

    if not valores_numericos:
        return "No se ha podido determinar un perfil claro para este grupo."

    promedio = sum(valores_numericos) / len(valores_numericos)

    if promedio >= 1.5:
        return "Este grupo muestra una alta afinidad general en los aspectos evaluados."
    elif promedio >= 0.75:
        return "Este grupo muestra una afinidad moderada en los aspectos evaluados."
    else:
        return "Este grupo muestra una baja afinidad general en los aspectos evaluados."


def procesar_grupo(grupo_id):
    close_old_connections()
    grupo = GrupoRLCP.objects.get(id=grupo_id)

    t_inicio = time.time()
    respuestas = obtener_respuestas_grupo(grupo)
    if not respuestas:
        print(f"Grupo {grupo.id}: sin respuestas válidas.")
        guardar_concepto_sin_testores(grupo.id, respuestas, "No se obtuvieron respuestas válidas del grupo.")
        return
    matriz = construir_matriz_diferencia(respuestas)
    if not matriz:
        print(f"Grupo {grupo.id}: matriz vacía.")
        guardar_concepto_sin_testores(grupo.id, respuestas, "Las respuestas del grupo son idénticas.")
        return

    # Extraemos testores: frecuencia → normal → relajado
    testores = extraer_testores_por_frecuencia(matriz)
    if not testores:
        print(f"Grupo {grupo.id}: no se encontraron testores por frecuencia. Intentando con método normal.")
    testores = extraer_testores(matriz)
    if not testores:
        print(f"Grupo {grupo.id}: intentando con método relajado.")
        testores = extraer_testores_relajados(matriz)
        if not testores:
            guardar_concepto_sin_testores(grupo.id, respuestas, "Las respuestas son demasiado dispersas o no forman un patrón distinguible.")
            return

    guardar_conceptos(grupo.id, respuestas, testores, matriz)
    print(f"Grupo {grupo.id} procesado en {time.time() - t_inicio:.2f} segundos")
def procesar_lc_conceptual_para_todos():
    try:
        grupos = GrupoRLCP.objects.all()
        lista_ids = [g.id for g in grupos]
        print(f"\n🔄 Procesando todos los grupos: {lista_ids}")
        if not lista_ids:
            print("⚠️ No se encontraron grupos para procesar.")
            return

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(procesar_grupo, lista_ids)

    except Exception as e:
        print(f"Error al procesar grupos: {e}")
