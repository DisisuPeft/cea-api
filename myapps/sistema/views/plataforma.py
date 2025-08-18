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
from myapps.estudiantes.models import Estudiante
from myapps.sistema.pagination import UsersPagination
from myapps.estudiantes.serializer import EstudianteSerializer
from django.db.models import Q
# Create your views here.

class ManageUsersview(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]), IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        # Se obtiene los usuarios a estudiante
        user = request.user
        q = (request.GET.get("q") or "").strip()
        
        
        queryset = (
            Estudiante.objects.exclude(user=user).select_related("user", "perfil", "lugar_nacimiento", "municipio").order_by("perfil__nombre", "perfil__apellidoP", "id")
        )
        
        if q:
            queryset = queryset.filter(
                Q(perfil__nombre__icontains=q) | Q(user__apellidoP__icontains=q)
            )
        
        # if not estudiantes:
        #     return Response("No existen estudiantes", status=status.HTTP_404_NOT_FOUND)
        
        paginator = UsersPagination()
        
        result = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = EstudianteSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
   
# class UpdateUsersView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [CustomJWTAuthentication]  
    
#     def get(self, request):
#         rols = request.user.roleID.all()
#         permisos = Permissions.objects.filter(permission__in=rols).distinct()
#         tabs = TabsModulo.objects.filter(permiso__in=permisos)
#         # print(permisos)
#         if not tabs:
#             return Response("Error al obtener al obtener los submenus, verifica con el administrador", status=status.HTTP_404_NOT_FOUND)
#         serializer = TabsModuloSerializer(tabs, many=True)
#         # print(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)









