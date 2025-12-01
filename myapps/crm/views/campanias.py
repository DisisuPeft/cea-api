
from myapps.authentication.models import UserCustomize as User
from django.http import JsonResponse
from django.utils.decorators import method_decorator  # importante
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from myapps.plataforma.permission import EsAutorORolPermitidoConRoles
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from rest_framework.viewsets import ModelViewSet
from myapps.crm.models import CampaniaPrograma
from myapps.crm.serializer import CampaniaProgramaSerializer
from django.utils.timezone import now
from django.db import transaction

# Create your views here.
# EN formularios siempre devolver el puro serializer 

class CampaniaViewSet(ModelViewSet):
    queryset = CampaniaPrograma.objects.all()
    serializer_class = CampaniaProgramaSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador", "Estudiante"]), EsAutorORolPermitidoConRoles(["Administrador"])]
    authentication_classes = [CustomJWTAuthentication]
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("campania", "programa")
        return qs
    
    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("La campaña fue creada con exito", status=status.HTTP_200_OK)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response("Campaña editada con exito.", status=status.HTTP_200_OK)
    

    @transaction.atomic
    def perform_update(self, serializer):

        instance = serializer.save()

        if hasattr(instance, "modified_by"):
            instance.modified_by = self.request.user
            instance.fecha_actualizacion = now()
            instance.save(update_fields=["modified_by", "fecha_actualizacion"])

        # Actualiza la Campania relacionada (modelo distinto)
        camp = instance.campania
        if camp:
            raw = self.request.data.get("body", None)
            if raw is not None:
                camp.activo = raw
                # opcional: sello de auditoría si existe
                if hasattr(camp, "modified_by"):
                    camp.modified_by = self.request.user
                if hasattr(camp, "fecha_actualizacion"):
                    camp.fecha_actualizacion = now()

                # Guarda solo los campos tocados
                update_fields = ["activo"]
                if hasattr(camp, "modified_by"):
                    update_fields.append("modified_by")
                if hasattr(camp, "fecha_actualizacion"):
                    update_fields.append("fecha_actualizacion")

                camp.save(update_fields=update_fields)

        return instance
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Campania eliminada con exito", status=status.HTTP_200_OK)                
        



