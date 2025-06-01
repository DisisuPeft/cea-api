from rest_framework import serializers
from ..models import ProgramaEducativo

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ["id", "nombre"]