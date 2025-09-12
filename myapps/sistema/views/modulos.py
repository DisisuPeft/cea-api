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
from myapps.perfil.serializer import ProfileSerializer
# from myapps.perfil.models import Profile
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
from myapps.sistema.serializer import ModulosSerializer, TabsModuloSerializer, PestaniaPlataformaSerializer
# Create your views here.

class Modulosview(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    
    
    def get(self, request, *args, **kwargs):
        user = request.user
        # print(user)
        # roles = user.roleID.all()
        
        modulos = Modulos.objects.filter(usuario=user.id).distinct().order_by('orden')
        # modulos_rol = Modulos.objects.filter(role__in=roles).distinct().order_by('orden')
        
        # modulos = (modulos_user | modulos_rol).distinct()
        # if modulos_user.exists() and modulos_rol.exists():
        #     modulos = (modulos_user | modulos_rol).distinct()
        # elif modulos_user.exists():
        #      modulos = modulos_user
        # else:
        #     modulos = modulos_rol
            
        if not modulos:
            return Response("menu not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ModulosSerializer(modulos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
class TabsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]  
    
    def get(self, request):
        user = request.user
        # print(permissions)
        # permisos = Permissions.objects.filter(permiso__in=user.permission.all()).distinct()
        tabs = TabsModulo.objects.filter(user=user.id).filter(modulo__id=6).distinct().order_by('orden')
        # tabs_permiso = TabsModulo.objects.filter(permiso__in=permissions).filter(modulo=id).distinct().order_by('orden')
        
        # print(tabs_user, tabs_permiso)
        if not tabs.exists():
            return Response("Error al obtener al obtener los submenus, verifica con el administrador", status=status.HTTP_404_NOT_FOUND)

        serializer = TabsModuloSerializer(tabs, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PestaniaEstudianteView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]  

    def get(self, request):
        user = request.user
        # permissions = user.permission.all()
        
        modulo = Modulos.objects.filter(usuario=user.id).first()
        # print(modulo)
        
        tabs = TabsModulo.objects.filter(user=user.id).filter(modulo=modulo.id).distinct().order_by('orden')
        # tabs_permiso = TabsModulo.objects.filter(permiso__in=permissions).filter(modulo=modulo.id).distinct().order_by('orden')
        
        
        # if tabs_user.exists() and tabs_permiso.exists():
        #     tabs = (tabs_user | tabs_permiso).distinct()
        # elif tabs_user.exists():
        #     tabs = tabs_user
        # else:
        #     tabs = tabs_permiso

        if not tabs:
            return Response("Error al obtener al obtener los submenus, verifica con el administrador", status=status.HTTP_404_NOT_FOUND)

        serializer = PestaniaPlataformaSerializer(tabs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AssignTabsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication] 
    
    def get(self, request, id):
        if not id:
            return Response("Not id provided", status=status.HTTP_400_BAD_REQUEST)
        
        tabs = TabsModulo.objects.filter(modulo__id=id)
        
        if not tabs:
            return Response("Submodules not found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = PestaniaPlataformaSerializer(tabs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
#         order_field = request.GET.get('sort_by', 'name')  # Valor por defecto 'name'
# if order_field.startswith('-'):
#     # Si es descendente
#     descending = True
#     order_field = order_field[1:]
# else:
#     descending = False