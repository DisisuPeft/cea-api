from django.shortcuts import render
from contextvars import Token

from myapps.authentication.manager import CustomUserManager
from myapps.authentication.models import UserCustomize as User, Permissions
from django.http import JsonResponse
from django.utils.decorators import method_decorator  # importante
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from myapps.perfil.serializers import ProfileSerializer
from myapps.perfil.models import Profile
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.sistema.models import Modulos, TabsModulo
from myapps.sistema.serializers import ModulosSerializer, TabsModuloSerializer
# Create your views here.

class Modulosview(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        # user = request.user.roleID.all()
        # print(user)
        modulos = Modulos.objects.filter(role__in=request.user.roleID.all()).distinct()
        if not modulos:
            return Response("Error al obtener el menu, verificar si existen", status=status.HTTP_404_NOT_FOUND)
        serializer = ModulosSerializer(modulos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
class TabsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]  
    
    def get(self, request):
        rols = request.user.roleID.all()
        permisos = Permissions.objects.filter(permission__in=rols).distinct()
        tabs = TabsModulo.objects.filter(permiso__in=permisos)
        print(permisos)
        if not tabs:
            return Response("Error al obtener el menu, verificar si existen", status=status.HTTP_404_NOT_FOUND)
        serializer = TabsModuloSerializer(tabs, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)











        
#         order_field = request.GET.get('sort_by', 'name')  # Valor por defecto 'name'
# if order_field.startswith('-'):
#     # Si es descendente
#     descending = True
#     order_field = order_field[1:]
# else:
#     descending = False