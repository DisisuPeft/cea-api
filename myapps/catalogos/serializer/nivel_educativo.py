from rest_framework import serializers
from ..models.niveleducativo import NivelEducativo
from .tipo_nivel import TipoNivelSerializer

class NivelEducativoSerializer(serializers.ModelSerializer):
    tipo_nivel = TipoNivelSerializer(required=False)
    class Meta:
        model = NivelEducativo
        fields = ["id", "name", "tipo_nivel"]