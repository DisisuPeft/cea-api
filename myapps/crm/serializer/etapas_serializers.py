from rest_framework import serializers
from ..models import Etapas


class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapas
        fields = '__all__'
        
        