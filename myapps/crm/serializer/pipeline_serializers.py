from rest_framework import serializers
from ..models import Pipline
from ..serializer import EtapaSerializer


class PipelineSerializer(serializers.ModelSerializer):
    # unidad_academica_nombre = serializers.CharField(source="instituciones_academicas.nombre", read_only=True) #sin logica
    unidad_academica_nombre = serializers.SerializerMethodField()
    programa_nombre = serializers.SerializerMethodField() #con logica
    etapas = EtapaSerializer(read_only=True, many=True)
    
    class Meta:
        model = Pipline
        fields = ["id", "nombre", "orden", "fecha_creacion", "fecha_actualizacion", "programa_nombre", "unidad_academica_nombre", "empresa", 'etapas']
     
    def get_programa_nombre(self, obj):        
        return obj.programa.nombre if obj.programa else None
    
    def get_unidad_academica_nombre(self, obj):        
        return obj.unidad_academica.nombre if obj.unidad_academica else None
    