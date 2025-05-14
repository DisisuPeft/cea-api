from rest_framework import serializers
from ..models import Notas


class NotasSerializer(serializers.ModelSerializer):
    # pipline = PipelineSerializer(read_only=True)
    usuario = serializers.SerializerMethodField()
    class Meta:
        model = Notas
        fields = ["id", "texto", "fecha_creacion", "usuario"]        
        
    
    def get_usuario(self, obj):
        if obj.usuario.profile: 
            return f"{obj.usuario.profile.nombre } {obj.usuario.profile.apellidoP}"
        else:
            None 