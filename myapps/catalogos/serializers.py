from rest_framework import serializers
from .models.niveleducativo import NivelEducativo
from .models.genero import Genero
from .models.tipo_nivel import TipoNivel

class TipoNivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNivel
        fields = ["id", "name"]
    
class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ["id", "name"]
        
class NivelEducativoSerializer(serializers.ModelSerializer):
    tipo_nivel = TipoNivelSerializer(required=False)
    class Meta:
        model = NivelEducativo
        fields = ["id", "name", "tipo_nivel"]