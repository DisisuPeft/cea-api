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
from ..serializer import LeadsSerializer, PipelineSerializer, EstatusSerializer, LeadCreateLandingSerializer
from django.utils import timezone
from django.db.models import Q

# Create your views here.
# EN formularios siempre devolver el puro serializer 
class LeadsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request, *args, **kwargs):
        # campania = self.define_campania()
        # print(campania.id)
        queryset = Lead.objects.all().select_related(
            'fuente', 'etapa', 'estatus', 'empresa', 'institucion'
        ).prefetch_related('notas', 'observaciones')
        
        if not queryset:
            return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeadsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LeadView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request, id):
        # campania = self.define_campania()
        # lead
        queryset = Lead.objects.filter(id=id).select_related(
            'fuente', 'etapa', 'estatus', 'empresa', 'institucion'
        ).prefetch_related('notas', 'observaciones')
        
        if not queryset:
            return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeadsSerializer(queryset[0])
        
        #Pipelines
        # print(queryset[0].etapa.pipline.id)
        p =  Pipline.objects.filter(id=queryset[0].etapa.pipline.id).prefetch_related('etapas')
        
        if not p:
            return Response("Pipeline query not found", status=status.HTTP_404_NOT_FOUND)

        pipeline = PipelineSerializer(p, many=True)
        
        estatus = Estatus.objects.all()
        
        if not estatus:
            return Response("Status query not found", status=status.HTTP_404_NOT_FOUND)
        estatus_serializer = EstatusSerializer(estatus, many=True)
        
        return Response({"lead": serializer.data, "pipeline": pipeline.data, "estatus": estatus_serializer.data}, status=status.HTTP_200_OK)

    def define_campania(self):
        now = timezone.now()
        # less than o equalt to lte    greater than or equal to gte
        # campania = Campania.objects.filter(
        #     Q(activa=1) & (Q(fecha_inicio__lte=now) & Q(fecha_fin__gte=now))            
        # ).first()
        # return campania
        campania_programa = CampaniaPrograma.objects.filter(
            
        )
        

class CreateLeadFromLanding(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        print(request.data)
        lead = {}
        
        for i in request.data:
            if i in request.data and request.data[i]:
                lead[i] = request.data[i]
        fuente = Fuentes.objects.get(id=4)
        etapa = Etapas.objects.get(id=1)
        estatus = Estatus.objects.get(id=1)
        if not fuente:
            return Response("Error al encontrar la fuente", status=status.HTTP_404_NOT_FOUND)
        if not etapa:
            return Response("Error al encontrar la etapa inicial del lead", status=status.HTTP_404_NOT_FOUND)
        if not estatus:
            return Response("Error al encontrar el estatus inicial del lead", status=status.HTTP_404_NOT_FOUND)
        lead['fuente'] = fuente.id
        lead['etapa'] = etapa.id
        lead['estatus'] = estatus.id
        lead_serializer = LeadCreateLandingSerializer(data=lead)
        if lead_serializer.is_valid():
            lead_serializer.save()
            return Response("En breve un asesor se pondra en contacto contigo", status=status.HTTP_200_OK)
        else: 
            return Response(lead_serializer.errors, status=status.HTTP_200_OK)