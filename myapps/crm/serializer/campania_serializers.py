from rest_framework import serializers
from ..models import Campania
from myapps.control_escolar.models import ProgramaEducativo
from ..models.campanias import CampaniaPrograma
from django.db import transaction
# from myapps.sistema.serializer import

    
class CampaniaProgramaSerializer(serializers.ModelSerializer):
    campania_r = serializers.SerializerMethodField()
    programa_r = serializers.SerializerMethodField()
    
    campania = serializers.PrimaryKeyRelatedField(read_only=True)
    programa = serializers.PrimaryKeyRelatedField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CampaniaPrograma
        fields = ["id", "campania", "programa", "campania_r", "programa_r", "costo_asignado", "unidad_academica", "usuario"]
    
    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
                
        if not request.data.get("nombre"):
            raise serializers.ValidationError("El nombre de la campaña es obligatorio.")
        
        campania_obj = {
            "nombre": request.data.get("nombre"),
            "fecha_inicio": request.data.get("fecha_inicio"),
            "fecha_fin": request.data.get("fecha_fin"),
            "activo": 1
        }
        
        try:
            campania = Campania.objects.create(**campania_obj)
        except Exception as e:
            raise serializers.ValidationError(f"No se pudo crear la campaña: {str(e)}")
        
        if not request.data.get("programa"):
            raise serializers.ValidationError("No se proporciono el identificador del programa")
        
        programa = ProgramaEducativo.objects.get(pk=request.data.get("programa"))
        
        if not programa:
            raise serializers.ValidationError("No se encontro el programa educativo, verifica la información.")
        
        validated_data['campania'] = campania
        validated_data['programa'] = programa
        validated_data['usuario'] = request.user
        
        return super().create(validated_data)  
    
    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']
        
        instance.modified_by = request.user
        
        return super().update(instance, validated_data) 
        
    def get_campania_r(self, obj):
        return {"id": obj.campania.id, "nombre": obj.campania.nombre, "fecha_inicio": obj.campania.fecha_inicio, "fecha_fin": obj.campania.fecha_fin, "activo": obj.campania.activo} if obj.campania else None

    def get_programa_r(self, obj):
        return {"id": obj.programa.id, "nombre": obj.programa.nombre, "imagen_url": obj.programa.imagen_url, "descripcion": obj.programa.descripcion} if obj.programa else None