from rest_framework import serializers
from ..models import Estudiante
from myapps.perfil.models.user_profile import User as Profile
from rest_framework.exceptions import ValidationError
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from django.db import transaction, IntegrityError
from myapps.catalogos.models import Genero, NivelEducativo


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
        fields = ["id", "nombre", "apellidoP", "apellidoM", "edad", "fechaNacimiento", "genero", "nivEdu","telefono", "user"]

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
        
    def get_lugar_nacimiento_name(self, obj):
        return {"id": obj.lugar_nacimiento.id, "name": obj.lugar_nacimiento.name} if obj.lugar_nacimiento else None
    
    # def get_municipio_name(self, obj):
    #     return obj.municipio.name if obj.municipio else None
class ProfileEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "nombre", "apellidoP", "apellidoM", "edad", "fechaNacimiento", "genero", "nivEdu","telefono"]

class EstudianteProfileSerializer(serializers.ModelSerializer):
    # lugar_nacimiento_name = serializers.SerializerMethodField()
    # municipio_name = serializers.SerializerMethodField()
    # user = serializers.CharField(required=False)
    perfil = ProfileEstudianteSerializer(required=False)
    class Meta:
        model = Estudiante
        fields = ["id", "curp", "rfc", "especialidad", "matricula", "lugar_nacimiento", "direccion", "tutor_nombre", "tutor_telefono", "activo", "grupo", "perfil", "municipio"]



class UpdateEstudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    curp = serializers.CharField(allow_null=True, required=False)
    rfc = serializers.CharField(allow_null=True, required=False)
    especialidad = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    lugar_nacimiento = serializers.IntegerField(allow_null=True, required=False)
    direccion = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    activo = serializers.IntegerField()
    perfil = serializers.DictField(write_only=True)
    municipio = serializers.IntegerField(allow_null=True, required=False)
    
    @transaction.atomic
    def update(self, instance, validated_data):
        perfil_obj = validated_data.pop('perfil')
        estado = validated_data.pop('lugar_nacimiento')
        municipio = validated_data.pop('municipio')
        
        user_obj = None
        if perfil_obj:
            user_obj = perfil_obj.pop("user", None)
        # Actualiza campos simples
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.lugar_nacimiento_id = estado
        instance.municipio_id = municipio
        instance.save()
        # Obtiene y resuelve referencias actuales y toleran None
        current_perfil = getattr(instance, "perfil", None)
        current_user = getattr(current_perfil, "user", None)
        # user_obj ---->request payload. lo que se captura de frontend
        # current_user ----> el usuario vinculado al perfil
        # 
        # 
        # 
        # Crea y edita usuario
        if user_obj is not None: #verifica el paylad
            email = (user_obj.pop("email", None) or "").strip().lower() #normaliza el email
            password = user_obj.pop("password", None) #obtiene el password
            roles = user_obj.pop("roleID", None) #obtiene los roles
            
            # verfica unicidad del usuario
            # Lo que pasa aqui es simple, validando que no venga un email de otro usuario, si existe entra en el exists, si no entra en el current pero devolviendo una lista vacia, haciendo que ya no entre en el exists
            if email:
                q = UserCustomize.objects.filter(email=email) #obtiene el usuario con el email que viene en la request
                if current_user: #verifica si current user existe--> esto viene de la relacion y verifica si el perfil ya tiene vinculado un usuario
                    # Si existe un usuario con una relacion al perfil#
                    q = q.exclude(pk=current_user.pk) 
                    #Excluye el usuario#
                if q.exists(): #si existe la primer query lanza un error de unicidad, ya que email es unique
                    raise serializers.ValidationError("El email ya esta registrado")
            
            if current_user is None:
                if not email:
                    raise serializers.ValidationError("Se necesita un email para crear al usuario")
                current_user = UserCustomize.objects.create_user(email=email, password=password)
                if roles is not None:
                    current_user.roleID.set(roles)

                if current_perfil is None:
                    if perfil_obj is None:
                        current_perfil = Profile.objects.create(user=current_user)
                    else:
                        current_perfil = Profile.objects.create(user=current_user, **perfil_obj)
                    instance.perfil = current_perfil
                    instance.save()
                else:
                    current_perfil.user = current_user
                    current_perfil.save()
            else:
                if email:
                    current_user.email = email
                if password:
                    current_user.set_password(password)
                current_user.save()
                if roles is not None:
                    current_user.roleID.set(roles)
        #
        # perfil_obj----> es el request del frontend
        # current_perfil ----> es la relacion con estudiante
        # 
        if perfil_obj is not None:
            perfil_id = perfil_obj.pop("id", None)
            genero_id = perfil_obj.pop('genero', None)
            nivEdu_id = perfil_obj.pop("nivEdu", None)
            
            v = perfil_obj.get("edad", None)
            if isinstance(v, str) and v.strip() == "":
                perfil_obj["edad"] = None
                
            if current_perfil is None:
                user_for_perfil = current_user
                kwargs = dict(perfil_obj)
                if user_for_perfil is not None:
                    kwargs["user"] = user_for_perfil
                current_perfil = Profile.objects.create(**kwargs)
                instance.perfil = current_perfil
                instance.save()
            else:
                for k, v in perfil_obj.items():
                    setattr(current_perfil, k, v)
                current_perfil.genero_id = genero_id
                current_perfil.nivEdu_id = nivEdu_id
                current_perfil.save()
        return instance
 
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