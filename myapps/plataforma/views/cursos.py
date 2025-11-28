from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
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
from myapps.control_escolar.serializer import ProgramaShowSerializer, ModuloEducativoViewSerializer
from myapps.control_escolar.pagination import ProgramaPagination
from myapps.control_escolar.models import Inscripcion
from myapps.plataforma.permission import EsAutorORolPermitido
from myapps.plataforma.serializer import InscripcionEstudianteSerializer
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
from django.db.models import Q

class CursoView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"]), EsAutorORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
# Faltaria agregar como medir el avance
    def get(self, request, *args, **kwargs):
        id = request.user.profile.estudiante.id if request.user else 0
        # print(id, request.user.profile)

        estudiante = Estudiante.objects.filter(id=id).first()

        if not estudiante:
            return Response("No existe relacion entre estudiante y usuario, consulta con el administrador", status=status.HTTP_404_NOT_FOUND)
        
        inscripciones = Inscripcion.objects.filter(estudiante=estudiante.id).select_related('campania_programa').order_by('-fecha_creacion').only('campania_programa__programa')
        # print(*inscripciones)
        if not inscripciones:
            return Response("No existen inscripciones", status=status.HTTP_404_NOT_FOUND)
        
        # programas = inscripciones.campania_programa.programa

        # if not programas:
        #     return Response("No existen programas", status=status.HTTP_404_NOT_FOUND)

        serializer = InscripcionEstudianteSerializer(inscripciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class CursoPaginatedView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, *args, **kwargs):
        id = request.user.profile.estudiante.id
        
        estudiante = Estudiante.objects.filter(id=id).first()
        if not estudiante:
            return Response("No existe relacion entre estudiante y usuario, consulta con el administrador", status=status.HTTP_404_NOT_FOUND)
        
        inscripciones = Inscripcion.objects.filter(estudiante=estudiante.id).select_related('campania_programa').order_by('-fecha_creacion').only('campania_programa__programa')
        # print(*inscripciones)
        if not inscripciones:
            return Response("No existen inscripciones", status=status.HTTP_404_NOT_FOUND)
        
        paginator = ProgramaPagination()
        
        result = paginator.paginate_queryset(queryset=inscripciones, request=request)
    
        
        serializer = InscripcionEstudianteSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    
class CursoPanelView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, id):
        accion = request.query_params.get("accion", None)
        user = request.user
        
        is_admin = bool(
            request
            and request.user.roleID.filter(name="Administrador").exists()
        )
        
        if accion == "modulos":
            return self.get_modulos(id, user, admin=is_admin)

        if accion == "actividades":
            return self.get_actividades(id)

        if accion == "comunidad":
            return self.get_comunidad(id)
        
        return self.get_curso(id, user, admin=is_admin)

    def get_modulos(self, id, user, admin):
        # curso = ProgramaEducativo.objects.filter(inscripcion__id=user.id).first()
        # modulos = ModuloEducativo.objects.filter(programa__id=curso.id)
        qs = ModuloEducativo.objects.all()
        if admin:
            modulos = qs.filter(programa__id=id)
        else:
            modulos = qs.filter(programa__inscripcion__id=user.profile.estudiante.id)
            
        serializer = ModuloEducativoViewSerializer(modulos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_actividades(self, id):
        # lógica para actividades
        return Response("obtiene actividades y examenes", status=status.HTTP_200_OK)

    def get_comunidad(self, id):
        # lógica para resumen
        return Response("obtiene comentarios de la comunidad", status=status.HTTP_200_OK)
    
    def get_curso(self, id, user, admin):
        qs = ProgramaEducativo.objects.all()
        
        if admin:
            curso = qs.filter(id=id).first()
        else:
            # print(user.id)
            curso = qs.filter(id=id, inscripcion__id=user.profile.estudiante.id).first()
            
        
        if not curso:
            return Response("Query not found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgramaShowSerializer(curso)
        return Response([serializer.data], status=status.HTTP_200_OK)
    
    
class CuntCursos(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        estudiante_user = request.user.profile.estudiante.id
        
        programas_count = Inscripcion.objects.filter(estudiante=estudiante_user).count()
        
        return Response(programas_count, status=status.HTTP_200_OK)
        


class CursosEstudianteModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Estudiante"]), EsAutorORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    queryset = ProgramaEducativo.objects.all().prefetch_related('campania_programa')
    serializer_class = ProgramaEducativoSerializer


    def get_queryset(self):
        estudiante_id = self.request.user.profile.estudiante.id
        programa_id = self.request.query_params.get("programa", None)

        qs = super().get_queryset()

        qs = qs.filter(campania_programa__inscripciones__estudiante=estudiante_id)
        print(qs)
        
        # action = self.request.query_params.get("action", None)
        # if action == "modulos":
        #     return self.get_modulos(programa_id=programa_id)
        
        return qs


    @action(detail=False, methods=["get"])
    def modulos(self, request):
        qs = ModuloEducativo.objects.all()
        modulos = qs.filter(programa__id=request.query_params.get("programa", None))
        serializer = ModuloEducativoViewSerializer(modulos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)