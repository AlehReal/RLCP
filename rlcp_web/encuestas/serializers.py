from rest_framework import serializers
from .models import LimeSurvey583965

from .models import GrupoRLCP


class LimeSurvey583965Serializer(serializers.ModelSerializer):
    class Meta:
        model = LimeSurvey583965
        fields = '__all__'


class GrupoRLCPSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoRLCP
        fields = '__all__'
