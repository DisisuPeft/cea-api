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
from ..serializer import LeadsSerializer, PipelineSerializer, EstatusSerializer, LeadCreateLandingSerializer, LeadRecentSerializer, VendedorSerializer, LeadsFormSerializar
from django.utils import timezone
from django.db.models import Q
from ..pagination import LeadPagination
from django.db.models import Count
from myapps.catalogos.models import InstitucionAcademica
from myapps.catalogos.serializer import InstitucionSerializarGeneric

# Create your views here.
# EN formularios siempre devolver el puro serializer 

class UnidadNegocioView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = request.user
        
        unidades = InstitucionAcademica.objects.filter(unidad_usuario=user.id)
        
        if not unidades:
            return Response("No se han asignado unidades de negocio", status=status.HTTP_403_FORBIDDEN)
        
        serializer = InstitucionSerializarGeneric(unidades, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        