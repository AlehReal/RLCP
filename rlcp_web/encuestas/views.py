from rest_framework.decorators import api_view
from rest_framework import generics
from .models import ( LimeSurvey583965, ConceptosGruposRLCP )
from .serializers import LimeSurvey583965Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .rlcp_processor import procesar_todo
from .models import GrupoRLCP
from .serializers import GrupoRLCPSerializer
from rest_framework import status
from .lc_conceptual import procesar_lc_conceptual_para_todos



class LimeSurveyListAPIView(generics.ListAPIView):
    queryset = LimeSurvey583965.objects.all()
    serializer_class = LimeSurvey583965Serializer

class GrupoRLCPListAPIView(generics.ListAPIView):
    queryset = GrupoRLCP.objects.all()
    serializer_class = GrupoRLCPSerializer

class ProcesarRLCPAPIView(APIView):
    def get(self, request, format=None):
        procesar_todo()  # Procesamiento completo
        return Response({"message": "Procesamiento RLCP completado correctamente."})

    def post(self, request, format=None):
        filtros = {
            k: v for k, v in {
                'provincia': request.data.get('provincia'),
                'universidad': request.data.get('universidad'),
                'carrera': request.data.get('carrera'),
            }.items() if v
        }   

        procesar_todo(filtros)
        return Response({"message": "Procesamiento con filtros completado correctamente."})
    
@api_view(['GET'])
def obtener_filtros_unicos(request):
    provincias = LimeSurvey583965.objects.values_list('provincia', flat=True).distinct()
    universidades = LimeSurvey583965.objects.values_list('universidad', flat=True).distinct()
    carreras = LimeSurvey583965.objects.values_list('carrera', flat=True).distinct()

    return Response({
        'provincias': sorted([p for p in provincias if p]),
        'universidades': sorted([u for u in universidades if u]),
        'carreras': sorted([c for c in carreras if c]),
    })

@api_view(['GET'])
def miembros_de_grupo(request, grupo_id):
    try:
        grupo = GrupoRLCP.objects.get(id=grupo_id)
        ids = [int(x) for x in grupo.ids_respuestas.split(',') if x.isdigit()]
        miembros = LimeSurvey583965.objects.filter(id__in=ids).values()
        return Response(list(miembros))
    except GrupoRLCP.DoesNotExist:
        return Response({'error': 'Grupo no encontrado'}, status=404)

@api_view(['GET'])
def obtener_conceptos_por_grupo(request, grupo_id):
    conceptos = ConceptosGruposRLCP.objects.filter(grupo_id=grupo_id)
    data = []

    for c in conceptos:
        data.append({
            "testor": c.testor.split(','),
            "concepto": c.concepto.split(','),
            "concepto_general": c.concepto_general.split(','),
            "recomendacion": c.recomendacion
        })

    return Response(data)


@api_view(['POST'])
def ejecutar_lc_conceptual(request):
    print("👉 Vista LC Conceptual llamada")
    try:
        procesar_lc_conceptual_para_todos()
        return Response({"mensaje": "Procesamiento LC Conceptual completado correctamente."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)