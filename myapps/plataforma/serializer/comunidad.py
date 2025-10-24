from rest_framework import serializers
from myapps.plataforma.models import Comentario


class ComentarioSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    respuestas = serializers.SerializerMethodField()
    
    class Meta:
        model = Comentario
        fields = [
            "id", "comentario", "editado", "status", "usuario", "fecha_creacion", "respuestas"
        ]
        read_only_fields=["usuario", "editado", "status"]
        
    def create(self, validated_data):
        request = self.context['request']
        validated_data['usuario'] = request.user
        validated_data['status'] = 1
        parent_raw = request.data.get('parent')
        
        if parent_raw not in {"null", "", None, "undefined"}:
            try:
                parent_id = int(parent_raw)
                padre = Comentario.objects.get(pk=parent_id)
                validated_data['padre'] = padre
            except (ValueError, Comentario.DoesNotExist):
                raise serializers.ValidationError("El comentario padre no existe")
            
        diplomado_id = request.query_params.get("diplomado")
        if diplomado_id:
            from myapps.control_escolar.models import ProgramaEducativo
            validated_data['diplomado'] = ProgramaEducativo.objects.get(pk=diplomado_id)
        else:
            raise serializers.ValidationError("El parámetro 'diplomado' es obligatorio.")
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "comentario" in validated_data and validated_data['comentario'] != instance.comentario:
            instance.editado = 1
            instance.modified_by = self.context['request'].user
        return super().update(instance, validated_data)
    
    
    def get_usuario(self, obj):
        perfil = getattr(obj.usuario, "profile", None)
        if perfil:
            return perfil.get_nombre_completo()
        return obj.usuario.email
    
    def get_respuestas(self, obj):
        serializer = ComentarioSerializer(obj.respuestas.all(), many=True)
        return serializer.data