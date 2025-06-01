from rest_framework import serializers
from ..models import Pipline
from ..serializer import EtapaSerializer


class PipelineSerializer(serializers.ModelSerializer):
    unidad_academica = serializers.SerializerMethodField()
    programa = serializers.SerializerMethodField() #con logica
    etapas = serializers.SerializerMethodField(read_only=True)
    empresa = serializers.SerializerMethodField()
    class Meta:
        model = Pipline
        fields = ["id", "nombre", "orden", "programa", "unidad_academica", "empresa", 'etapas']
     
    def get_programa(self, obj):        
        return {'id': obj.programa.id, 'nombre': obj.programa.nombre} if obj.programa else None
    
    def get_unidad_academica(self, obj):        
        return {'id': obj.unidad_academica.id, 'nombre': obj.unidad_academica.nombre} if obj.unidad_academica else None
    
    def get_etapas(self, obj):
     return [
        {'id': etapa.id, 'nombre': etapa.nombre, 'orden': etapa.orden}
        for etapa in obj.etapas.all()
    ]
     
    def get_empresa(self, obj):
        return {'id': obj.empresa.id, 'nombre': obj.empresa.nombre} if obj.empresa else None