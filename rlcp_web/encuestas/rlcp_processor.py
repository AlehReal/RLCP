from .models import LimeSurvey583965
from django.db import connection
from concurrent.futures import ThreadPoolExecutor

PREGUNTAS = [
    'edad', 'sexo', 'provincia', 'universidad', 'tipo_de_curso', 'carrera', 'año_academicco',
    'becado', 'trabajas', 'relacion_de_trabajo',
    'number_583965x17x432',
    'number_583965x17x433sq001', 'number_583965x17x433sq002',
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
    'number_583965x21x436sq031', 'number_583965x21x436sq032',
    'number_583965x20x430', 'number_583965x20x430comment'
]

def calcular_semejanza_lista(a, b):
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)

def calcular_fila_matriz(i, vectores):
    fila = []
    for j in range(len(vectores)):
        if i == j:
            fila.append(1.0)
        else:
            sim = calcular_semejanza_lista(vectores[i], vectores[j])
            fila.append(sim)
    return i, fila

def calcular_umbral(matriz):
    """Calcula el umbral de semejanza usando el algoritmo 'mínimo de los máximos' (sin contar la diagonal)"""
    if not matriz or all(len(fila) == 0 for fila in matriz):
        raise ValueError("Matriz vacía o sin filas válidas")

    maximos_por_fila = []
    for i, fila in enumerate(matriz):
        max_val = max(fila[j] for j in range(len(fila)) if j != i)  # ignorar la diagonal
        maximos_por_fila.append(max_val)

    umbral = min(maximos_por_fila)
    
    print(f"Máximos por fila (sin incluir diagonal): {maximos_por_fila}")
    print(f"Umbral calculado (mínimo de los máximos): {umbral}")
    
    return umbral


def matriz_semejanza_paralela(vectores):
    n = len(vectores)
    matriz = [None] * n
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(calcular_fila_matriz, i, vectores) for i in range(n)]
        for future in futures:
            i, fila = future.result()
            matriz[i] = fila
    return matriz


def beta_cero_compacto(registros, matriz, umbral):
    grupos = []
    usados = set()
    for i, fila in enumerate(matriz):
        if i in usados:
            continue
        grupo = [i]
        usados.add(i)
        for j, sim in enumerate(fila):
            if j != i and sim >= umbral and j not in usados:
                grupo.append(j)
                usados.add(j)
        grupos.append(grupo)
    return grupos

def calcular_patron_promedio_lista(grupo):
    patron = []
    for i in range(len(PREGUNTAS)):
        respuestas = [registro[i] for registro in grupo if registro[i] is not None]
        if respuestas:
            respuesta_mas_frecuente = max(set(respuestas), key=respuestas.count)
            patron.append(respuesta_mas_frecuente)
        else:
            patron.append(None)
    return patron

LOTE_TAMANO = 1000

def procesar_lote_simple(respuestas_lote, ids_lote):
    try:
        print(f"Procesando lote de {len(respuestas_lote)} registros...")
        print("Ejemplo de vectores:")
        for i in range(min(3, len(respuestas_lote))):
            print(f"{i}: {respuestas_lote[i][:5]}")

        # Calcular la matriz completa SIN aplicar ningún umbral
        matriz = matriz_semejanza_paralela(respuestas_lote)

        # Calcular umbral real con base en la matriz
        umbral = calcular_umbral(matriz)
        print(f"Umbral calculado: {umbral}")

        # Agrupar con base en la matriz y el umbral
        grupos = beta_cero_compacto(respuestas_lote, matriz, umbral)

        # Generar resultados
        resultados = []
        for grupo_indices in grupos:
            grupo_ids = [ids_lote[i] for i in grupo_indices]
            grupo_respuestas = [respuestas_lote[i] for i in grupo_indices]
            patron = calcular_patron_promedio_lista(grupo_respuestas)
            resultados.append((grupo_ids, patron))
        return resultados

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error procesando lote con IDs: {ids_lote[:5]}... → {e}")
        return []


def procesar_lotes_paralelo(filtros=None):
    queryset = LimeSurvey583965.objects.all()

    if filtros:
        if filtros.get('provincia'):
            queryset = queryset.filter(provincia=filtros['provincia'])
        if filtros.get('universidad'):
            queryset = queryset.filter(universidad=filtros['universidad'])
        if filtros.get('carrera'):
            queryset = queryset.filter(carrera=filtros['carrera'])

    registros = list(queryset.values_list('id', *PREGUNTAS))
    total = len(registros)
    print(f"Total registros: {total}")
    lotes = [registros[i:i + LOTE_TAMANO] for i in range(0, total, LOTE_TAMANO)]
    print(f"Procesando {len(lotes)} lotes...")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futuros = []
        for lote in lotes:
            ids = [r[0] for r in lote]
            respuestas = [list(r[1:]) for r in lote]
            futuros.append(executor.submit(procesar_lote_simple, respuestas, ids))

        with connection.cursor() as cursor:
            for future in futuros:
                resultados_lote = future.result()
                for grupo_ids, patron in resultados_lote:
                    ids_str = ",".join(str(i) for i in grupo_ids)
                    patron_str = ",".join(p if p is not None else '' for p in patron)
                    cantidad = len(grupo_ids)
                    cursor.execute(
                        "INSERT INTO grupos_rlcp (ids_respuestas, patron_promedio, cantidad_miembros) VALUES (%s, %s, %s)",
                        [ids_str, patron_str, cantidad]
                    )
    print("¡Procesamiento por lotes completado!")

def procesar_todo(filtros=None):
    procesar_lotes_paralelo(filtros)
