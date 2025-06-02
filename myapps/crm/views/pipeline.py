from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework import generics, status
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from ..models import Pipline, Etapas
from ..serializer import PipelineSerializer, PipelineSerializerCreate, PipelineSerializerUpdate
from django.utils import timezone
from django.db.models import Q
from myapps.control_escolar.models import ProgramaEducativo
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
from myapps.catalogos.models import InstitucionAcademica
from myapps.catalogos.serializer import InstitucionSerializarGeneric
from myapps.sistema.models import Empresa
from myapps.sistema.serializer import EmpresaSerializerGenerics
from ..serializer import EtapaSerializer
# Create your views here.
# EN formularios siempre devolver el puro serializer 
class PipelineAllView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        
        pipeline = Pipline.objects.all().prefetch_related('etapas')
        # print(pipeline)
        if not pipeline:
            return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = PipelineSerializer(pipeline, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        validated_data = {}
        for payload in request.data:
            if payload in request.data and request.data[payload]:
                validated_data[payload] = request.data[payload]
        validated_data['orden'] = 0
        # print(validated_data)
        serializer = PipelineSerializerCreate(data=validated_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("Pipeline creada con exito", status=status.HTTP_201_CREATED)
    
class PipelineUpdateView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def patch(self, request, id):
        if not id:
            return Response("El id no es viene en el request.", status=status.HTTP_400_BAD_REQUEST)

        pipeline = Pipline.objects.get(id=id)
        
        if not pipeline:
            return Response("not query found.", status=status.HTTP_404_NOT_FOUND)
        
        serializer = PipelineSerializerUpdate(pipeline, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("Pipeline editado con exito", status=status.HTTP_200_OK)
    
class GetProgramsView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        programs = ProgramaEducativo.objects.filter(activo=1)
        if not programs:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramaEducativoSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetUnidadAcademicaView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        instituto = InstitucionAcademica.objects.filter(activa=1)
        if not instituto:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = InstitucionSerializarGeneric(instituto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetEmpresaView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        empresa = Empresa.objects.filter(activa=1).filter(id=1)
        if not empresa:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = InstitucionSerializarGeneric(empresa, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetEtapasPipelineView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Vendedor"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, id):
        etapas = Etapas.objects.filter(pipline=id)
        if not etapas:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = EtapaSerializer(etapas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)