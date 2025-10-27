from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from django.db.models import Q
from myapps.plataforma.models import EnlaceClase, PlataformasImparticion
from myapps.plataforma.serializer import EnlaceSerializer, PlataformaImparticionSerializer
from myapps.plataforma.permission import EsAutorORolPermitidoConRoles
from django.utils import timezone

class EnlaceViewSet(ModelViewSet):
    queryset = EnlaceClase.objects.all()
    serializer_class = EnlaceSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"]), EsAutorORolPermitidoConRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    
    def get_queryset(self):
        qs = super().get_queryset()
        programa_id = self.request.query_params.get("programa")
        # is_admin = self.request.user.roleID.filter(name="Administrador").exists()
        
        if programa_id:
            qs = qs.filter(programa__id=programa_id)
        # if not is_admin:
        #     today = timezone.now().date()
        #     qs = qs.filter(fecha_imparticion__gte=today)
        return qs

        
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Enlace para la clase creado con exito", status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response("Enlace editada con exito", status=status.HTTP_200_OK)
    
    def destroy(self, instance):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Recurso eliminado con exito", status=status.HTTP_200_OK)
    
    
class PlataformaViewSet(ModelViewSet):
    queryset = PlataformasImparticion.objects.all()
    serializer_class = PlataformaImparticionSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"]), EsAutorORolPermitidoConRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    pagination_class = None
    
    def get_queryset(self):
        return super().get_queryset()