from rest_framework import serializers
from ..models import Etapas


class EtapaSerializer(serializers.ModelSerializer):
    # pipline = PipelineSerializer(read_only=True)
    class Meta:
        model = Etapas
        fields = '__all__'
        
        