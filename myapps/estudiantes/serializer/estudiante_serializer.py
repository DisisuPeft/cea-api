from rest_framework import serializers
from ..models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    lugar_nacimiento = serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "matricula", "lugar_nacimiento", "direccion", "telefono", "tutor_nombre", "tutor_telefono", "activo", "grupo", "nivel_educativo", "user", "fecha_actualizacion", "fecha_creacion", "email", "perfil", "municipio"]
        
    def get_lugar_nacimiento(self, obj):
        return obj.lugar_nacimiento.name if obj.lugar_nacimiento else None