from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.catalogos.models import (Municipios, EstadosRepublica, Especialidades, EstatusMaestro)
from myapps.catalogos.serializer import EstadosRepublicaSerializer, MunicipiosSerializer, MetodoPagoSerializer
from myapps.maestros.serializer import EspecialidadViewSerializer, EstatusViewSerializer
from myapps.control_escolar.permission import EsOwnerORolPermitido
from myapps.catalogos.models import MetodoPago
# from django.utils.timezone import now
# Create your views here.

class EstadosRepublicaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador", "Estudiante"]),  IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        entidades = EstadosRepublica.objects.all()
        if not entidades:
            return Response("No existen generos registrados", status=status.HTTP_404_NOT_FOUND)
        serializer = EstadosRepublicaSerializer(entidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MunicipioView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador", "Estudiante"]),  IsAuthenticated]
    
    def get(self, request, id):
        # entidad_id = request.GET.get('id')
        # print(id)
        municipios = Municipios.objects.filter(estado=id)
        if not municipios:
            return Response("Not found municipios", status=status.HTTP_404_NOT_FOUND)
        serializer = MunicipiosSerializer(municipios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class EspecialidadView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        especialidades = Especialidades.objects.all()
        if not especialidades:
            return Response("No existen especialidades", status=status.HTTP_404_NOT_FOUND)
        serializer = EspecialidadViewSerializer(especialidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EstatusView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        estatus_maestro = EstatusMaestro.objects.all()
        if not estatus_maestro:
            return Response("No existe un estatus para asignar a un docente", status=status.HTTP_404_NOT_FOUND)
        serializer = EstatusViewSerializer(estatus_maestro, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class MetodoPagoModelViewSet(ModelViewSet):
    queryset = MetodoPago.objects.all().only('id', 'nombre')
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    
    
    def get_queryset(self):
        # paginated = self.request.query_params.get('paginated')
        # print(paginated)
        qs =  super().get_queryset()
        
        qs = qs.order_by('-fecha_creacion')
        
        return qs