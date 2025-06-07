from myapps.authentication.models import UserCustomize, Roles, Permissions
from rest_framework import serializers
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from myapps.sistema.models.modulo import Modulos
from myapps.sistema.models.tabs_module import TabsModulo
from myapps.authentication.serializers import RoleCustomizeSerializer, PermissionCustomizeSerializer, UserCustomizeSerializer

class ModulosSerializer(serializers.ModelSerializer):
    # role = RoleCustomizeSerializer(many=True, required=False)
    class Meta:
        model = Modulos
        fields = ["id", "name", "description", "icon","bgColor", "textColor", "route", "orden"]
        
        

class TabsModuloSerializer(serializers.ModelSerializer):
    modulo = ModulosSerializer(required=False)
    permiso = PermissionCustomizeSerializer(many=True, required=False)
    # user = UserCustomizeSerializer(many=True, required=False)
    class Meta:
        model = TabsModulo
        fields = ["id", "name", "description", "modulo", "permiso", "href", "icon", "orden"]


