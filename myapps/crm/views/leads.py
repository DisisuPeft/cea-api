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
from ..models import Lead, CampaniaPrograma, Pipline, Estatus, Fuentes, Etapas, Request
from ..serializer import LeadsSerializer, PipelineSerializer, EstatusSerializer, RequestAddSerializer, LeadRecentSerializer, VendedorSerializer, LeadsFormSerializar, RequestSerializer
from django.utils import timezone
from django.db.models import Q
from ..pagination import LeadPagination, RequestPagination
from django.db.models import Count
from myapps.sistema.models import Empresa

# Create your views here.
# EN formularios siempre devolver el puro serializer 

class RequestView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request):
        user = request.user
        # unidad = request.GET.get("unidad")
        admin = user.roleID.filter(name="Administrador").first()
        empresa = request.GET.get("empresa")
        
        if admin:
            queryset = Request.objects.filter(Q(empresa__nombre=empresa)).select_related(
                'fuente', 'producto_interes', 'interesado_en', 'institucion'
            ).order_by("-fecha_creacion")
        
        request_paginator = RequestPagination()
              
        self.calculate_time_response(queryset=queryset)
        
        if not queryset:
            return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        
        result = request_paginator.paginate_queryset(queryset=queryset, request=request)
        
        serializer = RequestSerializer(result, many=True)
        
        return request_paginator.get_paginated_response(serializer.data)
    
    def calculate_time_response(self, queryset):
        for i in queryset:
            now = timezone.now()
            date_estimated =  now - i.fecha_creacion
            i.tiempo_primera_respuesta = date_estimated
            i.save()
            


            
class EstadisticsLeadsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        unidad = request.GET.get("unidad")
        empresa = request.GET.get("empresa")
        
        leads_count = Lead.objects.filter(institucion__id=unidad).count()
        total_lead_etapa = Lead.objects.filter(institucion__id=unidad).values('etapa__nombre').annotate(total=Count('id'))
        total_lead_programa = Lead.objects.filter(institucion__id=unidad).values('interesado_en__nombre').annotate(total=Count('id'))
        if not leads_count:
            return Response("There are not countable leads", status=status.HTTP_400_BAD_REQUEST)
        if not total_lead_etapa:
            return Response("There are not countable leads for stage", status=status.HTTP_400_BAD_REQUEST)
        if not total_lead_programa:
            return Response("There are not countable leads for program", status=status.HTTP_400_BAD_REQUEST) 
        
        data = {
            'total_leads': leads_count,
            'total_lead_etapa': total_lead_etapa,
            'total_lead_programa': total_lead_programa
        }
        return Response(data, status=status.HTTP_200_OK)
    
class LeadsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    # select_related -- para relacion 1 a 1 y 1 a M // prefetch -- para many to many e inversa
    def get(self, request, *args, **kwargs):
        user = request.user
        unidad = request.GET.get("unidad")
        admin = user.roleID.filter(name="Administrador").first()
        salesman = user.roleID.filter(name="Vendedor").first()
        
        if admin:
            queryset = Lead.objects.filter(Q(institucion__id=unidad)&Q(vendedor_asignado__isnull=False)).select_related(
                'fuente', 'etapa', 'estatus', 'empresa', 'institucion'
            ).prefetch_related('notas', 'observaciones').order_by('-fecha_creacion')
        if salesman:
            queryset = Lead.objects.filter(Q(institucion__id=unidad) & Q(vendedor_asignado__id=user.id)).select_related(
                'fuente', 'etapa', 'estatus', 'empresa', 'institucion'
            ).prefetch_related('notas', 'observaciones').order_by('-fecha_creacion')

        
        
        paginator = LeadPagination()
        result = paginator.paginate_queryset(queryset=queryset, request=request)
        
        self.calculate_time_response(queryset=queryset)
        
        if not queryset:
            return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeadsSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
    def calculate_time_response(self, queryset):
        for i in queryset:
            if i.etapa.nombre == "Interesado":
                now = timezone.now()
                date_estimated =  now - i.fecha_creacion
                i.tiempo_primera_respuesta = date_estimated
                i.save()
    
    def post(self, request):
        if not request.data:
            return Response("The request is empty", status=status.HTTP_400_BAD_REQUEST)
        # print(request.data)
        serializer = LeadsFormSerializar(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Lead creado con exito", status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response("Error al crear el lead", status=status.HTTP_400_BAD_REQUEST)

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
        serializer = RequestAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request = serializer.save()
        return Response("Gracias por registrarte, en breve un asesor se pondra en contacto contigo", status=status.HTTP_200_OK)
        
        
        
class GetVendedoresView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        user = User.objects.filter(roleID__name="Vendedor")
        
        if not user:
            return Response("no query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = VendedorSerializer(user, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)