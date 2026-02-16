from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.control_escolar.models import ProgramaEducativo
from rest_framework.viewsets import ModelViewSet
from myapps.control_escolar.permission import EsOwnerORolPermitido, EsOwnerORolPermitidoConRoles
from myapps.control_escolar.serializer import ProgramaEducativoCatalogSerializer, InscripcionSerializer
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.control_escolar.models import Inscripcion
from myapps.control_escolar.models import Pago
from django.db import transaction
from myapps.authentication.models import Roles
from django.shortcuts import get_object_or_404
from myapps.control_escolar.services.repositories.fichas import FichasService
from myapps.crm.models import CampaniaPrograma
from myapps.estudiantes.models import Estudiante, estudiante
from django.utils import timezone
from myapps.control_escolar.services import PagoService, ProgramaService
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
from rest_framework.decorators import action
from myapps.perfil.models import User as Profile
from myapps.authentication.models import UserCustomize
from django.db.models import Q
from myapps.control_escolar.models import Fichas, Comisiones
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
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, HasRoleWithRoles(["Administrador" ,"Vendedor"])])
    def applyficha(self, request):
        campania_programa_id = request.query_params.get('campania')
        print(campania_programa_id)
        data = request.data.copy()
        perfil = data.pop('perfil')
        precios = data.pop('precios')

        if not campania_programa_id:
            return Response(
                {"detail": "Se requieren los parámetros de la campaña"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            CampaniaPrograma.objects.get(pk=campania_programa_id)
        except CampaniaPrograma.DoesNotExist:
            return Response(
                {"detail": "Campaña-Programa no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not data.get('curp'):
            return Response(
                {"detail": "No se proporciono la curp."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for p in perfil:
            if not perfil[p]:
                return Response(
                    {"detail": "No se aceptan campos vacios del perfil."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # primero se verifica si el email se encuentra en la BD
        user_find = UserCustomize.objects.filter(email=data['email']).exists()
        if not user_find:
            # Despues busca si existe el perfil a partir de match con los campos del nombre completo
            perfil_find = (Profile.objects.filter(
                Q(nombre=perfil['nombre']) &
                Q(apellidoP=perfil['apellidoP']) &
                Q(apellidoM=perfil['apellidoM'])).exists())
            if perfil_find:
                return Response({"detail": "El perfil ya existe en los registros."}, status=status.HTTP_400_BAD_REQUEST)
            new_perfil = Profile.objects.create(**perfil)
            estudiante_find = Estudiante.objects.filter(curp=data['curp']).exists()
            if estudiante_find:
                new_perfil.delete()
                return Response({'detail': 'El curp del estudiante ya existe en los registros.'}, status=status.HTTP_400_BAD_REQUEST)
            estudiante_create = Estudiante.objects.create(perfil=new_perfil, **data)

            inscripcion_data = {}

            if precios.get('tiene_precio_custom'):
                precios_custom = precios.get('precios_custom', {})
                inscripcion_data.update({
                    'tiene_precio_custom': True,
                    'costo_inscripcion_acordado': precios_custom.get('costo_inscripcion'),
                    'costo_mensualidad_acordado': precios_custom.get('costo_mensualidad'),
                    'costo_documentacion_acordado': precios_custom.get('costo_documentacion'),
                    'notas_precio_custom': precios.get('razon_precio_custom')
                })


            serializer = self.get_serializer(data=inscripcion_data)
            serializer.is_valid(raise_exception=True)

            inscripcion = serializer.save(
                estudiante=estudiante_create,
                campania_programa_id=campania_programa_id
            )

            duracion_meses = inscripcion.campania_programa.programa.duracion_meses
            if duracion_meses is None:
                inscripcion.delete()
                estudiante_create.delete()
                new_perfil.delete()

                return Response(
                    {"detail": "Duración de meses no encontrada. Debes definir primero la duración del programa"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            pago_service = PagoService(inscripcion)

            resultado = pago_service.procesar_pago_inicial(
                monto=precios['monto'],
                notas=precios['notas'],
                conceptos_ids=precios['tipo_pago'],
            )
            coherencia_conceptos = pago_service.validar_coherencia_conceptos(
                conceptos_ids=precios['tipo_pago'],
                monto=precios['monto'],
            )
            print(resultado)
            # costos_reales = pago_service.obtener_costos_reales()
            if not resultado['success']:
                inscripcion.delete()
                estudiante_create.delete()
                new_perfil.delete()
                return Response({'detail': resultado['message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # print(coherencia_conceptos, resultado)
                if coherencia_conceptos['tiene_inscripcion']:
                    ficha = Fichas.objects.create(
                        estudiante=estudiante_create,
                        campania_programa_id=campania_programa_id,
                        vendedor=request.user,
                    )
                    Comisiones.objects.create(
                        ficha=ficha,
                        monto=coherencia_conceptos['costo_inscripcion']
                    )
                    return Response({'message': resultado['message']} ,status=status.HTTP_200_OK)
                else:
                    inscripcion.delete()
                    estudiante_create.delete()
                    new_perfil.delete()
                    return Response({'detail': 'El alumno no cuenta con inscripcion'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Este email ya se encuentra registrado en el sistema'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated, HasRoleWithRoles(["Administrador" ,"Vendedor"])])
    def fichas(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_final = request.query_params.get('fecha_final')

        fichas = FichasService.get_fichas(request.user.id)
        total_comision = FichasService.get_fichas_total_amount(request.user.id, fecha_inicio=fecha_inicio, fecha_fin=fecha_final)
        return Response({'fichas': fichas, 'totalComision': total_comision}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated, HasRoleWithRoles(['Administrador', "Tutor"])])
    def programas_inscripcion(self, request):
        estudiante_id = request.query_params.get('identificador')
        programas = ProgramaService.get_programa_inscripcion(int(estudiante_id))
        return Response(programas, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated, HasRoleWithRoles(['Administrador' ,"Tutor"])])
    def autorizar_ficha(self, request):
        switch_value = request.data.get('value')
        # print(switch_value)
        id_str = request.query_params.get('identificador')
        id_ficha = request.query_params.get('ficha')

        if switch_value == "off":
            return Response(
                {"detail": "No se permite desactivar la ficha."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar y convertir ID
        try:
            id_int = int(id_str)
        except (ValueError, TypeError):
            return Response(
                {"detail": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar y convertir ID
        try:
            ficha_int = int(id_ficha)
        except (ValueError, TypeError):
            return Response(
                {"detail": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        ficha = Fichas.objects.get(id=ficha_int)
        # Obtener estudiante
        estudiante = get_object_or_404(Estudiante, id=id_int)
        perfil = Profile.objects.filter(estudiante=estudiante).first()
        # Crear usuario
        user = UserCustomize.objects.create(email=estudiante.email)
        # user.profile = estudiante.perfil
        perfil.user = user
        perfil.save()
        # Asignar rol
        try:
            role = Roles.objects.get(name="Estudiante")
            user.roleID.add(role)  # O user.roleID.set([role])
        except Roles.DoesNotExist:
            return Response(
                {"detail": "Rol Estudiante no existe"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Establecer contraseña
        user.set_password("UNSZA.123")
        user.save()  # ← No olvides guardar
        estudiante.activo = 1
        ficha.autorizado = 1
        ficha.autorizado_by = request.user
        ficha.save()
        estudiante.save()
        return Response(
            {"message": "Ficha autorizada exitosamente"},
            status=status.HTTP_200_OK
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


