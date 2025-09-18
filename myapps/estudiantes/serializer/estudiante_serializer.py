from rest_framework import serializers
from ..models import Estudiante
from myapps.perfil.models.user_profile import User as Profile
from rest_framework.exceptions import ValidationError
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from django.db import transaction, IntegrityError


class UserEstudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[]) 
    password = serializers.CharField(
        write_only=True,
        required=False,
        error_messages={
            'blank': "El campo contraseña no puede estar vacío.",
            'required': "La contraseña es obligatoria."
        }
    )
    class Meta:
        model = UserCustomize
        fields = ["id", "email", "password", "roleID"]
        # extra_kwargs = {
        #     # Evita que el UniqueValidator automático dispare en nested-update
        #     "email": {"validators": []},
        # }
    
    # def create(self, validated_data):        
    #     password = validated_data.pop("password", None)
    #     user = UserCustomize.objects.create_user(**validated_data, password=password)
    #     roles = self.initial_data.get("roleID")
    #     if roles is not None:
    #         user.roleID.set(roles)
    #     return user
    
    # def update(self, instance, validated_data):
    #     roles = validated_data.pop('roleID', None)
    #     password = validated_data.pop("password", None)
        
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
        
    #     if password:
    #         instance.set_password(password)
            
    #     instance.save()
        
    #     if roles is not None:
    #         instance.roleID.set(roles)
        
    #     return instance
            
    def validate_email(self, value):
        user = getattr(self, "instance", None)
        qs = UserCustomize.objects.filter(email=value)
        if user:
            qs = qs.exclude(pk=user.id)
        if qs.exists():
            raise serializers.ValidationError("user with this email already exists.")
        return value

class ProfileEditSerializer(serializers.ModelSerializer):
    user = UserEstudentSerializer(required=False)
    class Meta:
        model = Profile
        fields = ["nombre", "apellidoP", "apellidoM", "edad", "fechaNacimiento", "genero", "nivEdu","telefono", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        email = user_data['email']
        password = user_data['password']
        user = UserCustomize.objects.create_user(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError({'user': "Usuario no creado"})
        
        profile = Profile.objects.create(user=user, **validated_data)
        
        return profile
        # profile = Profile.objects.create(**validated_data, user=)        
class EstudianteSerializer(serializers.ModelSerializer):
    # lugar_nacimiento_name = serializers.SerializerMethodField()
    # municipio_name = serializers.SerializerMethodField()
    # user = serializers.CharField(required=False)
    perfil = ProfileEditSerializer(required=False)
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "rfc", "especialidad", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "perfil", "municipio"]
    
    @transaction.atomic
    def create(self, validated_data):
        perfil_data = validated_data.pop("perfil", None)
        # user_data = None
        if perfil_data:
            user_data   = perfil_data.pop("user", None)

        for k in ("curp", "rfc", "matricula", "email"):
            if k in validated_data:
                validated_data[k] = validated_data[k] or None

        user = None
        if user_data:
            roles    = user_data.pop("roleID", [])
            password = user_data.pop("password", None)
            email    = (user_data.pop("email", None) or "").strip().lower()
            if not email:
                raise serializers.ValidationError({"user": {"email": ["El email es obligatorio."]}})

            user = UserCustomize.objects.filter(email=email).first()
            if user is None:
                user = UserCustomize.objects.create_user(email=email, password=password)
            else:
                for attr, val in user_data.items():
                    setattr(user, attr, val)
                if password:
                    user.set_password(password)
                user.save()


            if roles is not None:
                user.roleID.set(roles)
        profile = None
        if perfil_data:
            if not user:
                raise serializers.ValidationError({"perfil": ["Para crear perfil se requiere un usuario."]})
            profile = Profile.objects.create(user=user, **perfil_data)

        estudiante = Estudiante.objects.create(
            **validated_data,  
            perfil=profile,
        )
        return estudiante
    
    @transaction.atomic
    def update(self, instance, validated_data):
        # 1) Extrae datos anidados tal como en tu create
        perfil_data = validated_data.pop("perfil", None)
        user_data = None
        if perfil_data:
            user_data = perfil_data.pop("user", None)


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