from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from myapps.estudiantes.serializer import EstudianteSerializer, EstudianteSerializerView, EstudianteEditSerializer
from myapps.authentication.decorators import role_required
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.estudiantes.models import Estudiante
from myapps.control_escolar.models import ProgramaEducativo, ModuloEducativo
from myapps.control_escolar.serializer import ProgramaEducativoCatalogSerializer, ProgramaEducativoCardSerializer, ProgramaShowSerializer, ModuloEducativoViewSerializer
from myapps.control_escolar.pagination import ProgramaPagination

class CursoView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]
# Faltaria agregar como medir el avance
    def get(self, request, *args, **kwargs):
        user = request.user
        
        estudiante = Estudiante.objects.filter(user=user.id).first()
        if not estudiante:
            return Response("No existe relacion entre estudiante y usuario, consulta con el administrador", status=status.HTTP_404_NOT_FOUND)
        
        programas = ProgramaEducativo.objects.filter(inscripcion=estudiante.id).order_by('-fecha_creacion')
        
        if not programas:
            return Response("No existen programas educativos", status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgramaShowSerializer(programas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class CursoPaginatedView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        estudiante = Estudiante.objects.filter(user=user.id).first()
        if not estudiante:
            return Response("No existe relacion entre estudiante y usuario, consulta con el administrador", status=status.HTTP_404_NOT_FOUND)
        
        programas = ProgramaEducativo.objects.filter(inscripcion=estudiante.id).order_by('-fecha_creacion')
        
        if not programas:
            return Response("No existen programas educativos", status=status.HTTP_404_NOT_FOUND)
        
        paginator = ProgramaPagination()
        
        result = paginator.paginate_queryset(queryset=programas, request=request)
    
        
        serializer = ProgramaShowSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    
class CursoPanelView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, id):
        accion = request.query_params.get("accion", None)

        if accion == "modulos":
            return self.get_modulos(id)

        if accion == "actividades":
            return self.get_actividades(id)

        if accion == "comunidad":
            return self.get_comunidad(id)
        
        return self.get_curso(id)

    def get_modulos(self, id):
        # lógica para módulos
        modulos = ModuloEducativo.objects.filter(programa__id=id)
        serializer = ModuloEducativoViewSerializer(modulos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_actividades(self, id):
        # lógica para actividades
        return Response("obtiene actividades y examenes", status=status.HTTP_200_OK)

    def get_comunidad(self, id):
        # lógica para resumen
        return Response("obtiene comentarios de la comunidad", status=status.HTTP_200_OK)
    
    def get_curso(self, id):
        curso = ProgramaEducativo.objects.get(id=id)
        if not curso:
            return Response("Query not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramaShowSerializer(curso)
        return Response([serializer.data], status=status.HTTP_200_OK)
    
    
class CuntCursos(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        estudiante_user = request.user.id
        
        programas_count = ProgramaEducativo.objects.filter(inscripcion=estudiante_user).count()
        
        return Response(programas_count, status=status.HTTP_200_OK)
        
        