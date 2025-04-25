from rest_framework import serializers
from ..models import Fuentes

class FuenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuentes
        fields = '__all__'

