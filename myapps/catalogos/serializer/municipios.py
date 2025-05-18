from rest_framework import serializers
from ..models import Municipios

class MunicipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipios
        fields = ["id", "nombre"]