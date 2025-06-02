from django.shortcuts import render
from contextvars import Token

from myapps.authentication.manager import CustomUserManager
from myapps.authentication.models import UserCustomize as User
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
# from myapps.perfil.models import User
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from ..models import Lead, CampaniaPrograma, Pipline, Estatus, Fuentes, Etapas
from ..serializer import EstatusSerializer, FuenteSerializer
from django.utils import timezone
from django.db.models import Q
from ..pagination import LeadPagination
from django.db.models import Count

# Create your views here.
# EN formularios siempre devolver el puro serializer 

class GetFuentesView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        fuentes = Fuentes.objects.all()
        if not fuentes:
            return Response("No existen fuentes", status=status.HTTP_404_NOT_FOUND)
        serializer = FuenteSerializer(fuentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = FuenteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("Fuente creada", status=status.HTTP_201_CREATED)


class UpdateFuentesView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def patch(self, request, id):
        if not id:
            return Response("El id no viene presente en la solicitud", status=status.HTTP_400_BAD_REQUEST)
        fuentes = Fuentes.objects.get(id=id)
        if not fuentes:
            return Response("La fuente que intentas actualizar no existe", status=status.HTTP_404_NOT_FOUND)
        
        serializer = FuenteSerializer(fuentes, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("Fuente editada con exito", status=status.HTTP_200_OK)
    
class GetEstatusView(APIView):
    
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        estatus = Estatus.objects.all()
        if not estatus:
            return Response("No existen estatus", status=status.HTTP_404_NOT_FOUND)
        serializer = EstatusSerializer(estatus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EstatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("Estatus creado", status=status.HTTP_201_CREATED)
    
    
class UpdateEstatusView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def patch(self, request, id):
        if not id:
            return Response("El id no viene presente en la solicitud", status=status.HTTP_400_BAD_REQUEST)
        estatus = Estatus.objects.get(id=id)
        if not estatus:
            return Response("La fuente que intentas actualizar no existe", status=status.HTTP_404_NOT_FOUND)
        
        serializer = EstatusSerializer(estatus, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("Estatus editado con exito", status=status.HTTP_200_OK)