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
from myapps.plataforma.models import Comentario
from myapps.plataforma.serializer import ComentarioSerializer
from myapps.plataforma.permission import EsAutorORolPermitidoConRoles
from myapps.control_escolar.models import ProgramaEducativo


class ComentarioViewSet(ModelViewSet):
    queryset = Comentario.objects.select_related("usuario", "diplomado").filter(status=1)
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"]), EsAutorORolPermitidoConRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]


    def get_queryset(self):
        qs = super().get_queryset()
        diplomado_id = self.request.query_params.get("diplomado")
        padre_id = self.request.query_params.get("padre")

        if diplomado_id:
            qs = qs.filter(diplomado__id=diplomado_id)
        if padre_id:
            qs = qs.filter(padre_id=padre_id)
        else:
            qs = qs.filter(padre__isnull=True)
        
        return qs

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Comentario creado con exito", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response("Comentario actualizado", status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.status = 99
        instance.comentario = ""
        instance.save(update_fields=["status", "comentario"])
        