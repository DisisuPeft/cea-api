from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import action
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.control_escolar.models import ProgramaEducativo
from rest_framework.viewsets import ModelViewSet
from myapps.control_escolar.permission import EsOwnerORolPermitido, EsOwnerORolPermitidoConRoles
from django.shortcuts import get_object_or_404
from myapps.control_escolar.models import SubModulo, TipoPago
from myapps.control_escolar.serializer import ProgramaEducativoCatalogSerializer
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.control_escolar.models import Inscripcion, Pago, TipoPago
from myapps.control_escolar.models import Pago
from django.db import transaction
from myapps.control_escolar.services import PagoService
from django.utils.timezone import now
from django.db.models import Sum, F, Q, DecimalField, ExpressionWrapper, Count, Case, When, Value, Prefetch
from django.db.models.functions import Coalesce
from myapps.estudiantes.models import Estudiante
from myapps.control_escolar.serializer import PagoSerializer, TipoPagoSerializer, EstudianteConInscripcionesSerializer
# Create your views here.

class TipoPagoViewSet(ModelViewSet):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    

    def get_queryset(self):
        qs = super().get_queryset()
        return qs    
            
            
class PagosModelViewSet(ModelViewSet):
    serializer_class = EstudianteConInscripcionesSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    
    def get_queryset(self):
        inscripciones_qs = Inscripcion.objects.select_related(
            'campania_programa__programa',
            'campania_programa__campania'
        ).prefetch_related(
            'pagos__tipo_pago'
        ).annotate(
            # Total pagado (no cambia)
            total_pagado_calc=Sum(
                'pagos__monto',
                filter=Q(pagos__estado='completado'),
                default=0
            )
        ).annotate(
            # Total requerido considerando precios custom
            total_requerido_calc=Case(
                # Si tiene precio custom, usa los acordados (con fallback a precios normales)
                When(
                    tiene_precio_custom=True,
                    then=ExpressionWrapper(
                        Coalesce(F('costo_inscripcion_acordado'), F('campania_programa__programa__costo_inscripcion')) +
                        (Coalesce(F('costo_mensualidad_acordado'), F('campania_programa__programa__costo_mensualidad')) * 
                        F('campania_programa__programa__duracion_meses')) +
                        Coalesce(F('costo_documentacion_acordado'), F('campania_programa__programa__costo_documentacion')),
                        output_field=DecimalField(max_digits=10, decimal_places=2)
                    )
                ),
                # Si no tiene precio custom, usa los precios del programa
                default=ExpressionWrapper(
                    F('campania_programa__programa__costo_inscripcion') +
                    (F('campania_programa__programa__costo_mensualidad') * 
                    F('campania_programa__programa__duracion_meses')) +
                    F('campania_programa__programa__costo_documentacion'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).annotate(
            # Saldo pendiente
            saldo_pendiente_calc=ExpressionWrapper(
                F('total_requerido_calc') - F('total_pagado_calc'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        inscripciones_prefetch = Prefetch(
            'inscripcion',  # Verifica el related_name correcto
            queryset=inscripciones_qs
        )
        
        qs = Estudiante.objects.annotate(
            total_inscripciones=Count('inscripcion', distinct=True)
        ).select_related(
            'perfil',
            'lugar_nacimiento',
            'municipio'
        ).prefetch_related(
            inscripciones_prefetch,
        ).filter(
            inscripcion__isnull=False 
        ).distinct()

        estudiante_id = self.request.query_params.get('estudiante_id')
        if estudiante_id:
            qs = qs.filter(id=estudiante_id)
        
        return qs
    

    def create(self, request):
        ins_id = request.query_params.get("ins")
        
        if not ins_id:
            return Response({"detail": "No se proveyo el identificador del inscrito"}, status=status.HTTP_400_BAD_REQUEST)
        tipo_pago = TipoPago.objects.get(pk=ins_id)
        print(tipo_pago)
        # try: 
        #     inscripcion = Inscripcion.objects.get(pk=ins_id)
        # except (Inscripcion.DoesNotExist):
        #     return Response({"detail": "La inscripcion no fue encontrada en la base de datos"}, status=status.HTTP_404_NOT_FOUND)
        
        # pago = Pago.objects.create(
        #     inscripcion=inscripcion,
        #     tipo_pago=request.data.get("tipo_pago"),
        #     fecha_pago=now(),
        #     estado="completado",
        #     metodo_pago=request.data.get("metodo_pago"),
        #     notas=request.data.get("notas"),
        #     monto=request.data.get("monto")
        # )
        # pago.save()
        return Response("Pago creado con exito", status=status.HTTP_200_OK)
    

    # action personalizado
    @action(detail=False, methods=['post'])
    def aplicar_pago(self, request):
        # inscripcion_id = request.query_params.get("ins")
        pago = PagoService.aplicar_pago(data=request.data, user=request.user)
        # print(pago)
        if not pago['success']:
            return Response({"message": pago['message']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": pago['message']}, status=status.HTTP_200_OK)
    
