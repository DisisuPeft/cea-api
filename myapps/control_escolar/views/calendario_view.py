from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from myapps.authentication.authenticate import CustomJWTAuthentication
from ..serializer import CicloSerializer, CicloSerializerQueryState
from ..pagination import CicloPagination
from myapps.catalogos.models import Ciclos
from django.db.models import Q
from django.utils import timezone
# Create your views here.


class GetCiclosView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        now = timezone.now()
        ciclos = Ciclos.objects.all().filter(
                Q(fecha_inicio__lte=now) & 
                Q(fecha_inicio__gte=now)
            )
        paginator = CicloPagination()
        
        result = paginator.paginate_queryset(queryset=ciclos, request=request)
        
        if not ciclos:
            return Response("Not query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = CicloSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
              
    def post (self, request):
        ciclo = {}
        for payload in request.data:
            if payload in request.data and request.data[payload]:
                ciclo[payload] = request.data[payload]
                
        serializer = CicloSerializer(data=ciclo)
        
        if not serializer.is_valid():
            return Response(f"Report error:{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response("El ciclo fue creado con exito", status=status.HTTP_201_CREATED)
        

class RetrieveCiclosParamView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        now = timezone.now()
        ciclos = Ciclos.objects.all().filter(
                Q(fecha_inicio__lte=now) & 
                Q(fecha_fin__gte=now) &
                Q(estado=1)
            )
        
        if not ciclos:
            return Response("Not query found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = CicloSerializerQueryState(ciclos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

     
class ObtainCiclosParamView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        q = request.GET.get('ciclo_id')
        if not q or q == 'NaN':
            return Response("No query param provided", status=status.HTTP_204_NO_CONTENT)
        
        ciclo = Ciclos.objects.filter(id=int(q)).first()
        serializer = CicloSerializer(ciclo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class GetCiclosParam(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    
    def get(self, request):
        now = timezone.now()
        ciclos = Ciclos.objects.all().filter(
            Q(fecha_inicio__lte=now) & 
            Q(fecha_inicio__gte=now)
        )