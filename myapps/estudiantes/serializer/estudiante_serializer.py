from rest_framework import serializers
from ..models import Estudiante
from myapps.perfil.models.user_profile import User as Profile
from rest_framework.exceptions import ValidationError
from myapps.perfil.serializer import ProfileSerializer, ProfileEditSerializer
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from django.db import transaction, IntegrityError

class UserEstudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustomize
        fields = ["id", "email", "password", "roleID"]


class EstudianteSerializer(serializers.ModelSerializer):
    # lugar_nacimiento_name = serializers.SerializerMethodField()
    # municipio_name = serializers.SerializerMethodField()
    # user = serializers.CharField(required=False)
    perfil = ProfileEditSerializer()
    user = UserEstudentSerializer()
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "rfc", "especialidad", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "email", "perfil", "municipio", "user"]
    
    def create(self, validated_data):
        perfil_data = validated_data.pop('perfil', None)
        user_data   = validated_data.pop('user', None)
        # print(user_data)
        try:
            with transaction.atomic():
                user = None
                if user_data:
                    user = UserCustomize.objects.create_user(
                        email=user_data['email'],
                        password=user_data['password'],
                    )
                    roles = user_data.get("roleID") or []
                    user.roleID.set(roles)

                profile = None
                if perfil_data:
                # Si tu Profile tiene FK/OneToOne a User y lo quieres amarrar:
                # perfil_data = { **perfil_data, "user": user }  # si el campo existe
                    profile = Profile.objects.create(**perfil_data, user=user)

                estudiante = Estudiante.objects.create(
                    **validated_data,
                    user=user,
                    perfil=profile,
                )

            return estudiante

        except IntegrityError as e:
            raise serializers.ValidationError({"user": "Email ya registrado"}) from e
    
    def update(self, instance, validated_data):
        perfil = validated_data.pop('perfil')
        usuario = validated_data.pop("user")
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        if perfil:
            existe = getattr(instance, "perfil", None)
            if existe:
                for attr, value in perfil.items():
                    setattr(instance.perfil, attr, value)
                instance.perfil.save()
            else:
                profile = Profile.objects.create(**perfil)
                instance.perfil = profile
                instance.save()
                
        if usuario:
            exist = getattr(instance, "usuario", None)
            if exist:
                for attr, value in usuario.items():
                    setattr(instance.user, attr, value)
                instance.user.save()
            else:
                user = UserCustomize.objects.create(**usuario)
                instance.user = user
                instance.save()
                
        return instance
        
    def get_lugar_nacimiento_name(self, obj):
        return {"id": obj.lugar_nacimiento.id, "name": obj.lugar_nacimiento.name} if obj.lugar_nacimiento else None
    
    # def get_municipio_name(self, obj):
    #     return obj.municipio.name if obj.municipio else None
    
class EstudianteSerializerView(serializers.ModelSerializer):
    lugar_nacimiento = serializers.SerializerMethodField()
    municipio = serializers.SerializerMethodField()
    perfil = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "rfc", "especialidad", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "user", "fecha_actualizacion", "fecha_creacion", "email", "perfil", "municipio"]
    
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
        fields = ["id", "rfc", "especialidad", "curp", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "user", "fecha_actualizacion", "fecha_creacion", "email", "perfil", "municipio"]
    
    def get_lugar_nacimiento(self, obj):
        return {"id": obj.lugar_nacimiento.id, "nombre": obj.lugar_nacimiento.name} if obj.lugar_nacimiento else None
    
    def get_municipio(self, obj):
        return {"id": obj.municipio.id, "nombre": obj.municipio.nombre} if obj.municipio else None