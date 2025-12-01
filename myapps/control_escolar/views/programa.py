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
from myapps.control_escolar.models import ProgramaEducativo
from rest_framework.viewsets import ModelViewSet
from myapps.control_escolar.permission import EsOwnerORolPermitido, EsOwnerORolPermitidoConRoles
from django.shortcuts import get_object_or_404
from myapps.control_escolar.models import SubModulo, TipoPago
from myapps.control_escolar.serializer import ProgramaEducativoCatalogSerializer, InscripcionSerializer
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.control_escolar.models import Inscripcion
from myapps.control_escolar.models import Pago
from django.db import transaction
from myapps.crm.models import CampaniaPrograma
from myapps.estudiantes.models import Estudiante
from django.utils import timezone
from myapps.control_escolar.services import PagoService
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
# Create your views here.

class ProgramaViewSet(ModelViewSet):
    queryset = ProgramaEducativo.objects.select_related('institucion', 'tipo', 'modalidad').all()
    serializer_class = ProgramaEducativoCatalogSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    
    def get_queryset(self):
        request = self.request
        estudiante_raw = request.query_params.get("estudiante_id")
        
        qs = super().get_queryset()
        
        estudiante_id = None
        if estudiante_raw and estudiante_raw.lower() not in {"null", "undefined", "none", "nan", ""}:
            try:
                estudiante_id = int(estudiante_raw)
            except (TypeError, ValueError):
                estudiante_id = None
            qs = qs.exclude(campania_programa__inscripciones__estudiante_id=estudiante_id)
            
        qs = qs.filter(campania_programa__campania__activo=1)
        # .distinct()
        
        qs = qs.prefetch_related('modulos', 'campania_programa')
        return qs
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response("Programa Editado", status=status.HTTP_200_OK)
        

class InscripcionModelViewSet(ModelViewSet):
    queryset = Inscripcion.objects.select_related('campania_programa', 'estudiante').prefetch_related('pagos').all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Administrador"]), EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    
    def get_queryset(self):
        qs = super().get_queryset()
    
        return qs

    @transaction.atomic
    def create(self, request):
        # 1. Validar parámetros requeridos
        estudiante_id = request.query_params.get("estudiante")
        campania_programa_id = request.query_params.get("campania-programa")
        
        if not campania_programa_id or not estudiante_id:
            return Response(
                {"detail": "Se requieren los parámetros del estudiante y de la campaña"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 2. Validar que existan los recursos
        try:
            CampaniaPrograma.objects.get(pk=campania_programa_id)
            Estudiante.objects.get(pk=estudiante_id)
        except (CampaniaPrograma.DoesNotExist, Estudiante.DoesNotExist):
            return Response(
                {"detail": "Estudiante o Campaña-Programa no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 3. Preparar datos de inscripción
        inscripcion_data = {}
        
        # Si hay precios custom, agregarlos
        if request.data.get('tiene_precio_custom'):
            precios = request.data.get('precios_custom', {})
            inscripcion_data.update({
                'tiene_precio_custom': True,
                'costo_inscripcion_acordado': precios.get('costo_inscripcion'),
                'costo_mensualidad_acordado': precios.get('costo_mensualidad'),
                'costo_documentacion_acordado': precios.get('costo_documentacion'),
                'notas_precio_custom': request.data.get('razon_precio_custom')
            })
        
        # 4. Crear inscripción
        serializer = self.get_serializer(data=inscripcion_data)
        serializer.is_valid(raise_exception=True)
        
        inscripcion = serializer.save(
            estudiante_id=estudiante_id,
            campania_programa_id=campania_programa_id
        )
        
        # 5. Validar duración de meses
        duracion_meses = inscripcion.campania_programa.programa.duracion_meses
        if duracion_meses is None:
            inscripcion.delete()
            return Response(
                {"detail": "Duración de meses no encontrada. Debes definir primero la duración del programa"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 6. Procesar el pago usando el servicio
        pago_service = PagoService(inscripcion)
        
        resultado = pago_service.procesar_pago_inicial(
            monto=request.data.get("monto"),
            notas=request.data.get("notas"),
            conceptos_ids=request.data.get("tipo_pago")  # Array de IDs de conceptos
        )
        
        # 7. Manejar resultado del servicio
        if not resultado["success"]:
            # Si falló, eliminar la inscripción creada
            inscripcion.delete()
            return Response(
                {"detail": resultado["message"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 8. Respuesta exitosa
        return Response(
            {
                "message": resultado["message"],
            },
            status=status.HTTP_201_CREATED
        )
    


class GetProgramasEstudianteView(APIView):
    permission_classes = [IsAuthenticated, HasRoleWithRoles(["Estudiante"]), EsOwnerORolPermitido]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request):
        estudiante_id = request.user.profile.estudiante.id
        programs = ProgramaEducativo.objects.filter(activo=1).prefetch_related('campania_programa').exclude(campania_programa__inscripciones__estudiante_id=estudiante_id)
        if not programs:
           return Response("No query found", status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramaEducativoSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)