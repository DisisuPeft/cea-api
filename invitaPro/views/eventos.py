from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from invitaPro.models import Evento
from myapps.authentication.views import CustomJWTAuthentication
from invitaPro.serializers import EventoSerializer, ItinerarioPasoSerializer
from invitaPro.permission import EsOwnerORolPermitidoConRoles, EsOwnerORolPermitido
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from invitaPro.models import ItinerarioPaso
from rest_framework.response import Response

class EventosModelViewSet(ModelViewSet):
    queryset = Evento.objects.all().select_related('estatus', 'tipo_producto')
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated, EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]

    
    
    def get_queryset(self):
        return super().get_queryset()
    
    
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)
    

class ItinerarioModelViewSet(ModelViewSet):
    queryset = ItinerarioPaso.objects.select_related("evento").all()
    serializer_class = ItinerarioPasoSerializer
    # permission_classes = [IsAuthenticated, EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    ordering = ("orden",)
    
    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)

    
    def get_authenticators(self):
        if self.action in ["list", "partial_update"]:
            return [] 
 
        return [auth() for auth in self.authentication_classes]
    
    def get_permissions(self):
        if self.action in ["list", "partial_update"]:
            # Permitir acceso público a retrieve y update
            permission_classes = [AllowAny]
        else:
            # Para las demás acciones (create, list, destroy) exige autenticación
            permission_classes = [IsAuthenticated, EsOwnerORolPermitido]
        return [permission() for permission in permission_classes]

    
    def get_queryset(self):
        qs = super().get_queryset()
        evento_id = self.request.query_params.get("evento")
        if evento_id:
            qs = qs.filter(evento_id=evento_id)
        return qs
    
    
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        
        def visible(p):
            desbloqueado_por_tiempo = p.is_unlocked()
            desbloqueado_por_password = getattr(p, "password_match", 0) == 1
            
            # print(f"Paso: {p.titulo}")
            # print(f"  - Tiempo: {desbloqueado_por_tiempo}")
            # print(f"  - Password: {desbloqueado_por_password}")
            # print(f"  - Visible: {desbloqueado_por_tiempo or desbloqueado_por_password}")
            
            return desbloqueado_por_tiempo or desbloqueado_por_password

        obj_visibles = [p for p in qs if visible(p)]

        serializer = self.get_serializer(obj_visibles, many=True)
        return Response(serializer.data)
    
    
    def perform_update(self, serializer):
        paso = self.get_object()
        user_password = self.request.data.get("q")

        
        if paso.include_password and paso.password:
            # p = paso.password.lower()
            # print(paso.password, user_password)
            if user_password != paso.password:
                raise serializers.ValidationError("Contraseña incorrecta.")

        serializer.save(
            password_match=1,
        )
    
    # def update(self, request, *args, **kwargs):
    #     iti = self.get_object()
    #     password = self.request.data.get("pass")
        
    #     if iti.include_passworod and iti.password:
            
    #     return super().update(request, *args, **kwargs)