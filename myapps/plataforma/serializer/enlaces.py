from rest_framework import serializers
from myapps.plataforma.models import EnlaceClase, PlataformasImparticion
from myapps.control_escolar.models import ProgramaEducativo

class EnlaceSerializer(serializers.ModelSerializer):
    plataforma_name = serializers.SerializerMethodField()
    
    class Meta:
        model = EnlaceClase
        fields = [
            "id", "programa", "link", "fecha_imparticion", "titulo", "descripcion", "plataforma", "plataforma_name", "password_platform"
        ]
        read_only_fields=["programa", "plataforma_name"]
        
    def create(self, validated_data):
        request = self.context['request']
        
        programa_id = request.query_params.get('programa')
        plataforma_id = request.data.get('plataforma')
        if programa_id:
            programa = ProgramaEducativo.objects.get(pk=programa_id)
            validated_data['programa'] = programa
        else:
            raise serializers.ValidationError("El identificador del programa no fue incluido en la solicitud.")
            
        validated_data['titulo'] = request.data.get('titulo')
        validated_data['link'] = request.data.get('link')
        validated_data['fecha_imparticion'] = request.data.get('fecha_imparticion')
        validated_data['password_platform'] = request.data.get("password")
        
        if plataforma_id:
            plataforma = PlataformasImparticion.objects.get(pk=plataforma_id)
            validated_data['plataforma'] = plataforma
        else:
            raise serializers.ValidationError("La plataforma donde se impartira el curso no fue compartida en la solicitud.")
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        if "link" in validated_data and validated_data["link"] != instance.link:
            instance.editado_por = request.user   
        return super().update(instance, validated_data)
    
    
    def get_plataforma_name(self, obj):
        return obj.plataforma.nombre if obj.plataforma else None
    
    # def get_respuestas(self, obj):
    #     serializer = ComentarioSerializer(obj.respuestas.all(), many=True)
    #     return serializer.data
    
    
class PlataformaImparticionSerializer(serializers.ModelSerializer):
    class Meta:
        model=PlataformasImparticion
        fields = ['id', 'nombre']