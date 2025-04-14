from rest_framework import serializers
from myapps.catalogos.serializer import GeneroSerializer, NivelEducativoSerializer
from ..models import User
from myapps.catalogos.models import Genero, NivelEducativo

class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.IntegerField(write_only=True, required=False)
    # genero = GeneroSerializer(required=False)
    # nivEdu = NivelEducativoSerializer(required=False)
    genero = serializers.PrimaryKeyRelatedField(queryset=Genero.objects.all(), write_only=True)
    genero_info = GeneroSerializer(source="genero", read_only=True)

    nivEdu = serializers.PrimaryKeyRelatedField(queryset=NivelEducativo.objects.all(), write_only=True)
    nivEdu_info = NivelEducativoSerializer(source="nivEdu", read_only=True)
    class Meta:
        model = User
        fields = ["nombre", "apellidoP", "apellidoM", "edad", "fechaNacimiento", "genero", "genero_info", "nivEdu", "nivEdu_info", "telefono", "user"]
        extra_kwargs = {field: {'required': False} for field in fields}
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.fechaNacimiento:
            data["fechaNacimiento"] = instance.fechaNacimiento.strftime("%d/%m/%Y")
        return data  
    
    def create(self, validated_data):
        user = validated_data.pop('user', None)
        
            # Crear el perfil
        profile = User.objects.create(**validated_data)
        
            # Asignar el usuario si existe
        if user:
            profile.user = user
            profile.save()
        
        return profile

    def update(self, instance, validated_data):
        # Actualizar todos los campos que vengan en validated_data
        # print(instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance