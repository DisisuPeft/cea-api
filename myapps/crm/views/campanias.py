from django.shortcuts import render
from contextvars import Token

from myapps.authentication.manager import CustomUserManager
from myapps.authentication.models import UserCustomize as User
from django.http import JsonResponse
from django.utils.decorators import method_decorator  # importante
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from ..models import Lead, CampaniaPrograma, Pipline, Estatus, Fuentes, Etapas, Campania
from ..serializer import LeadsSerializer, PipelineSerializer, EstatusSerializer, LeadRecentSerializer, VendedorSerializer, CampaniaSerializer
from django.utils import timezone
from django.db.models import Q
from ..pagination import LeadPagination
from django.db.models import Count

# Create your views here.
# EN formularios siempre devolver el puro serializer 

class CampaniaView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        time = timezone.now()
        campanias = Campania.objects.filter(
            Q(fecha_inicio__lte=time) & Q(fecha_fin__gte=time)
        ).prefetch_related('programa_campania')
        
        if not campanias:
            return Response("no query found", status=status.HTTP_400_BAD_REQUEST)

        serializer = CampaniaSerializer(campanias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

