from rest_framework import serializers
from ..models import EstadosRepublica

class EstadosRepublicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadosRepublica
        fields = ["id", "name"]