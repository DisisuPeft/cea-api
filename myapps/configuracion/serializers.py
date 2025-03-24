from myapps.authentication.models import UserCustomize, Roles, Permissions
from rest_framework import serializers
from myapps.perfil.models import Profile
from myapps.perfil.serializers import ProfileSerializer
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from myapps.configuracion.models import MenuItems
from myapps.authentication.serializers import RoleCustomizeSerializer

class MenuItemSerializer(serializers.ModelSerializer):
    role = RoleCustomizeSerializer(many=True, required=False)
    class Meta:
        model = MenuItems
        fields = ["id", "name", "description", "icon", "itemCount", "bgColor", "textColor", "route", "role"]
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field = 'email'

#     def validate(self, attrs):
#         credentials = {
#             'email': attrs.get('email'),
#             'password': attrs.get('password')
#         }
#         user = authenticate(**credentials)
#         if user: 
#             if not user.is_active:
#                 raise exceptions.AuthenticationFailed('User is deactivated')


# class RoleCustomizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Roles
#         fields = ["id", "name"]

#         def create(self, validated_data):
#             role = Roles.objects.create(
#                 name=validated_data['name'],
#             )
#             role.save()
#             return role


# class PermissionCustomizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permissions
#         fields = ["id", "name"]
#         def create(self, validated_data):
#             permission = Permissions.objects.create(
#                 name=validated_data['name'],
#             )
#             permission.save()
#             return permission

# class UserCustomizeSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer(required=False) #para que me devuelva al usuario
#     role = serializers.ListField(
#         child=serializers.IntegerField(),  # Cada elemento debe ser un entero
#         required=False,  # No es obligatorio
#         allow_empty=True  # Permite una lista vacía
#     )
#     roleID = RoleCustomizeSerializer(many=True, required=False) #para devolver el rol en la respuesta
#     email = serializers.CharField(
#         required=True,
#         error_messages={
#             'blank': "El email del usuario no puede estar vacío.",
#             'required': "El email del usuario es obligatorio."
#         }
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         error_messages={
#             'blank': "El campo contraseña no puede estar vacío.",
#             'required': "La contraseña es obligatoria."
#         }
#     )
#     class Meta:
#         model = UserCustomize
#         fields = ["id", "email", "password", "profile", "role", "roleID"]

#     def create(self, validated_data):
#         role_ids = validated_data.pop('role', [])
#         # print(role_id)
#         # print(validated_data)
#         try:
#             with transaction.atomic():

#                 user = UserCustomize.objects.create_user(
#                     email=validated_data['email'],
#                     password=validated_data['password'],
#                 )
#                 if role_ids:
#                     try:
#                         roles = Roles.objects.filter(id__in=role_ids)
#                         if len(roles) != len(role_ids):
#                             raise serializers.ValidationError("Uno o más roles no existen")
                    
#                     # Agregar múltiples roles
#                         user.roleID.add(*roles)
                
#                     except Roles.DoesNotExist:
#                         raise serializers.ValidationError("Alguno de los roles especificados no existe")
            
#                 return user
#         except Exception as e:
#             raise serializers.ValidationError(str(e))

#     # def update(self, instance, validated_data):
#     #     print(instance)
#     #     roles = validated_data.pop('role', [])
#     #     # print(role)
#     #     if 'password' in validated_data:
#     #         instance.set_password(validated_data['password'])
#     #         validated_data.pop('password')
        
#     #     instance = super().update(instance, validated_data)

#     #     # print(instance.role)

#     #     return instance

#     def validate_email(self, value):
#         if UserCustomize.objects.filter(email=value).exists():
#             raise serializers.ValidationError("El email ya se encuentra registrado")
#         return value


