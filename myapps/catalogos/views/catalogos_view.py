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
from myapps.catalogos.models import (Municipios, EstadosRepublica)
from myapps.catalogos.serializer import EstadosRepublicaSerializer, MunicipiosSerializer

# Create your views here.

class EstadosRepublicaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        entidades = EstadosRepublica.objects.all()
        if not entidades:
            return Response("No existen generos registrados", status=status.HTTP_404_NOT_FOUND)
        serializer = EstadosRepublicaSerializer(entidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MunicipioView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request, id):
        # entidad_id = request.GET.get('id')
        # print(id)
        municipios = Municipios.objects.filter(estado=id)
        if not municipios:
            return Response("Not found municipios", status=status.HTTP_404_NOT_FOUND)
        serializer = MunicipiosSerializer(municipios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)