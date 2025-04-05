from myapps.authentication.models import UserCustomize, Roles, Permissions
from rest_framework import serializers
from myapps.perfil.models import Profile
from myapps.perfil.serializers import ProfileSerializer
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from myapps.sistema.models import MenuItems
from myapps.authentication.serializers import RoleCustomizeSerializer

class MenuItemSerializer(serializers.ModelSerializer):
    role = RoleCustomizeSerializer(many=True, required=False)
    class Meta:
        model = MenuItems
        fields = ["id", "name", "description", "icon", "itemCount", "bgColor", "textColor", "route", "role"]



