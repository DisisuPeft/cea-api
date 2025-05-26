from rest_framework import serializers
from ..models import Estudiante
from rest_framework.exceptions import ValidationError
from myapps.perfil.serializer import ProfileSerializer

class EstudianteSerializer(serializers.ModelSerializer):
    # lugar_nacimiento_name = serializers.SerializerMethodField()
    # municipio_name = serializers.SerializerMethodField()
    perfil = ProfileSerializer()
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "user", "fecha_actualizacion", "fecha_creacion", "email", "perfil", "municipio"]
    
    def create(self, validated_data):
        profile_id = validated_data.pop('perfil')
        # print(validated_data)
        estudiante = Estudiante.objects.create(**validated_data)
        if not estudiante:
            raise ValidationError("Estudiante no creado")
        estudiante.perfil = profile_id #instancia
        estudiante.save()
        return estudiante
    
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
        
    def get_lugar_nacimiento_name(self, obj):
        return obj.lugar_nacimiento.name if obj.lugar_nacimiento else None
    
    # def get_municipio_name(self, obj):
    #     return obj.municipio.name if obj.municipio else None
    
class EstudianteSerializerView(serializers.ModelSerializer):
    lugar_nacimiento = serializers.SerializerMethodField()
    municipio = serializers.SerializerMethodField()
    perfil = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "user", "fecha_actualizacion", "fecha_creacion", "email", "perfil", "municipio"]
    
    def get_lugar_nacimiento(self, obj):
        return obj.lugar_nacimiento.name if obj.lugar_nacimiento else None
    
    def get_municipio(self, obj):
        return obj.municipio.nombre if obj.municipio else None
    
class EstudianteEditSerializer(serializers.ModelSerializer):
    lugar_nacimiento = serializers.SerializerMethodField()
    municipio = serializers.SerializerMethodField()
    perfil = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "user", "fecha_actualizacion", "fecha_creacion", "email", "perfil", "municipio"]
    
    def get_lugar_nacimiento(self, obj):
        return {"id": obj.lugar_nacimiento.id, "nombre": obj.lugar_nacimiento.name} if obj.lugar_nacimiento else None
    
    def get_municipio(self, obj):
        return {"id": obj.municipio.id, "nombre": obj.municipio.nombre} if obj.municipio else None