from rest_framework import serializers
from ..models.tipo_nivel import TipoNivel

class TipoNivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNivel
        fields = ["id", "name"]