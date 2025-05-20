from rest_framework import serializers
from myapps.maestros.models import Maestro
from myapps.catalogos.models import Especialidades
from myapps.catalogos.models import EstatusMaestro
from rest_framework.exceptions import ValidationError
from myapps.perfil.models import User as Perfil
from myapps.perfil.serializer import ProfileSerializer

class MaestroSerializerForm(serializers.ModelSerializer):
    perfil = ProfileSerializer()
    class Meta:
        model = Maestro
        fields = ["id", "rfc", "fecha_ingreso", "numero_colaborador", "telefono", "direccion", "activo", "especialidad", "user", "fecha_actualizacion", "fecha_creacion", "curp", "email", "perfil", "estado", "estatus", "municipio"]
    
    def create(self, validated_data):
        # user_data = validated_data.pop('user')
        perfil_data = validated_data.pop('perfil')
        
        if not validated_data:
            raise ValidationError("request data not found")
        
        # if not user_data:
        #     pass
        if not perfil_data:
            raise ValidationError("Informacion personal vacia")
        perfil = Perfil.objects.create(**perfil_data)
        # print(perfil)
        if not perfil:
            raise ValidationError("El perfil no pudo ser creado")
        maestro = Maestro.objects.create(perfil=perfil,**validated_data)
        if not maestro:
            raise ValidationError("El maestro no pudo ser creado")
        return maestro
    
    def update(self, instance, validated_data):
        perfil = validated_data.pop('perfil')
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        if perfil:
            for attr, value in perfil.items():
                setattr(instance.perfil, attr, value)
            instance.perfil.save()
        return instance

class MaestroSerializerView(serializers.ModelSerializer):
    especialidad = serializers.SerializerMethodField()
    perfil = ProfileSerializer()
    estado = serializers.SerializerMethodField()
    municipio = serializers.SerializerMethodField()
    estatus = serializers.SerializerMethodField()
    
    class Meta:
        model = Maestro
        fields = '__all__'
    def get_estado(self, obj):
        return obj.estado.name if obj.estado else None
    def get_municipio(self, obj):
        return obj.municipio.nombre if obj.municipio else None
    def get_especialidad(self, obj):
        return obj.especialidad.name if obj.especialidad else None
    def get_estatus(self, obj):
        return obj.estatus.name if obj.estatus else None
       
class EspecialidadViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Especialidades
        fields = ["id", "name"]
        
        
class EstatusViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatusMaestro
        fields = ["id", "name"]