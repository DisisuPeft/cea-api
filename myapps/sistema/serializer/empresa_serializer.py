from myapps.authentication.models import UserCustomize, Roles, Permissions
from rest_framework import serializers
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from django.db import transaction
from myapps.sistema.models import Empresa



class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


