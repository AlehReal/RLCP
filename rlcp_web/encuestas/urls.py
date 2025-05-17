from django.urls import path
from .views import (
    LimeSurveyListAPIView,
    ProcesarRLCPAPIView,
    GrupoRLCPListAPIView,
    obtener_filtros_unicos,
    miembros_de_grupo,
    obtener_conceptos_por_grupo,
    ejecutar_lc_conceptual
)

urlpatterns = [
    path('respuestas/', LimeSurveyListAPIView.as_view(), name='lime-survey-list'),
    path('procesar/', ProcesarRLCPAPIView.as_view(), name='procesar-rlcp'),
    path('grupos/', GrupoRLCPListAPIView.as_view(), name='grupos-rlcp'),
    path('filtros-opciones/', obtener_filtros_unicos, name='filtros-opciones'),
    path('grupos/<int:grupo_id>/miembros/', miembros_de_grupo, name='miembros-grupo'),
    path('grupos/<int:grupo_id>/conceptos/', obtener_conceptos_por_grupo, name='conceptos-por-grupo'),
    path('lc-conceptual/', ejecutar_lc_conceptual, name='lc-conceptual'),
]
