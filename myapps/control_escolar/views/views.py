from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.control_escolar.models import ProgramaEducativo
from ..serializer import ProgramaEducativoCatalogSerializer
from ..pagination import ProgramaPagination
from myapps.control_escolar.serializer import ProgramaEducativoSerializer, ProgramaEducativoLandingSerializer, ProgramaShowSerializer, ModuloEducativoViewSerializer, SubModuloViewSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from myapps.control_escolar.models import SubModulo

# Create your views here.


class GetProgramasCatalogView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    def get(self, request, *args, **kwargs):
        programas = ProgramaEducativo.objects.all().order_by('-fecha_creacion')
        
        paginator = ProgramaPagination()
        
        result = paginator.paginate_queryset(queryset=programas, request=request)
        
        if not programas:
            return Response("No existen programas educativos", status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgramaEducativoCatalogSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
        

class GetProgramsRequestView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        programs = ProgramaEducativo.objects.filter(activo=1)
        if not programs:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramaEducativoSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetProgramLandingView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        programas = ProgramaEducativo.objects.filter(activo=1)
        if not programas:
            return Response("No se encontraron los programas educativos", status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramaEducativoLandingSerializer(programas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetProgramaView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id: int):

        programa = get_object_or_404(
            ProgramaEducativo.objects.filter(activo=1)
            .prefetch_related('modulos__submodulos'),  
            pk=id
        )


        try:
            modulos_qs = programa.modulos.all()
        except AttributeError:
            modulos_qs = programa.moduloeducativo_set.all()

        # submodulos_qs = SubModulo.objects.filter(modulo__in=modulos_qs)

      
        programa_ser = ProgramaShowSerializer(programa)
        modulos_ser = ModuloEducativoViewSerializer(modulos_qs, many=True)
        # submods_ser = SubModuloViewSerializer(submodulos_qs, many=True)

    
        return Response(
            {
                "programa": programa_ser.data,
                "modulos": modulos_ser.data,       
            },
            status=status.HTTP_200_OK
        )
    
    
class GetProgramasView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        programs = ProgramaEducativo.objects.filter(activo=1)
        if not programs:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramaShowSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class ProgramaEducativoModelViewSet()