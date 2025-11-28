from rest_framework import serializers
from ..models import ProgramaEducativo, TipoPrograma, ModuloEducativo, SubModulo
from myapps.estudiantes.models import Estudiante
from myapps.perfil.models import User as Profile
from myapps.catalogos.models import InstitucionAcademica
from myapps.crm.models import CampaniaPrograma
from myapps.control_escolar.models import Inscripcion
from django.db import transaction
from myapps.crm.models import Campania
# from myapps.control_escolar.serializer import PagoSerializer


class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ["id", "nombre", "imagen_url", "banner_url", "descripcion"]
        
class ProgramaEducativoLandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ["id", "nombre", "descripcion", "imagen_url", "banner_url"]


   
class PerfilInscritosSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    class Meta:
        model = Profile
        fields = ["id", "fullname"]
        
    def get_fullname(self, obj):
        return f"{obj.nombre} {obj.apellidoP} {obj.apellidoM or ''}" if obj.nombre and obj.apellidoP else None          


class InscritosSerializer(serializers.ModelSerializer):
    nombre_completo = PerfilInscritosSerializer()
    class Meta:
        model = Estudiante
        fields = ["id", "nombre_completo"]   
   
        
class ProgramaEducativoCardSerializer(serializers.ModelSerializer):
    # tipo = 
    inscritos = InscritosSerializer(many=True, read_only=True)
    class Meta:
        model = ProgramaEducativo
        fields = [
            'id',
            'nombre',
            'descripcion',
            'tipo',
            'institucion',
            'duracion_horas',
            'activo',
            'inscritos'
        ]
    
class InstitucionProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = [
            "nombre"
        ]

class ProgramaShowSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()
    modalidad = serializers.SerializerMethodField()
    inscrito = serializers.SerializerMethodField()
    
    class Meta:
        model = ProgramaEducativo
        fields = [
            'id',
            'nombre',
            'descripcion',
            'tipo',
            'duracion_horas',
            'modalidad',
            'banner_url',
            "imagen_url",
            "inscrito"
        ]
        

    def get_tipo(self, obj):
        return obj.tipo.nombre if obj.tipo else None
    
    def get_modalidad(self, obj):
        return obj.modalidad.name if obj.modalidad else None

    def get_inscrito(self, obj):
        return bool(getattr(obj, "inscrito", False))
    
    
class SubModuloViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubModulo
        fields = [
            "id", "titulo", "descripcion", 
            "orden", "path_class"
        ] 
       
class ModuloEducativoViewSerializer(serializers.ModelSerializer):
    submodulos = SubModuloViewSerializer(required=False, many=True)
    class Meta:
        model = ModuloEducativo
        fields = ["id", "nombre", "horas_teoricas", "horas_practicas", "horas_totales", "creditos", "submodulos"]
        
        
        
class ProgramaEducativoCatalogSerializer(serializers.ModelSerializer):
    modulos_list = serializers.SerializerMethodField()
    campania_programa = serializers.SerializerMethodField()

    class Meta:
        model = ProgramaEducativo
        fields = [
            'id',
            'nombre',
            'descripcion',
            'tipo',
            'institucion',
            'duracion_horas',
            'fecha_inicio',
            'fecha_fin',
            'horario',
            'costo_inscripcion',
            'costo_mensualidad',
            'costo_documentacion',
            'activo',
            'maestro',
            "duracion_meses",
            'modalidad',
            'fecha_creacion',
            'fecha_actualizacion',
            'periodo_imparticion',
            'banner_url',
            'imagen_url',
            # Relaciones hacia hijos
            'dirigido',
            'publico_objetivo',
            'perfil_ingreso',
            'requisitos_actitudinales',
            'requisitos_deseables',
            'enfoque_pedagogico',
            'requisito_ingreso',
            'requisito_permanencia',
            'requisito_egreso',
            'perfil_egreso',
            'resultado_aplicacion',
            'resultado_actualizacion',
            'resultado_crecimiento',
            'justificacion',
            'modulos',
            'campania_programa',
            'modulos_list',
        ]
    
    def get_modulos_list(self, obj):
        return ModuloEducativoViewSerializer(obj.modulos.all(), many=True).data
    
    def get_campania_programa(self, obj):
        # Import tardío para evitar el ciclo
        from myapps.crm.serializer import CampaniaProgramaSerializer
        qs = obj.campania_programa.all()
        return CampaniaProgramaSerializer(qs, many=True).data
    
    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']
        instance.modified_by = request.user
        return super().update(instance, validated_data)
        
class EstudianteSerializer(serializers.ModelSerializer):
    especialidad = serializers.CharField(source='especialiadad.nombre', read_only=True)
    lugar_nacimiento = serializers.CharField(source='lugar_nacimiento.nombre', read_only=True)
    municipio = serializers.CharField(source='municipio.nombre', read_only=True)
    perfil = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = fields = ["curp", "rfc", "especialidad", "lugar_nacimiento", "direccion", "activo", "perfil", "municipio"]        
      
    def get_perfil(self, obj):
        return f"{obj.perfil.nombre} {obj.perfil.apellidoP} {obj.perfil.apellidoM}"
    

class CamapaniaSerializer(serializers.ModelSerializer):
    campania = serializers.SerializerMethodField()
    programa = serializers.SerializerMethodField()
    class Meta:
        model = CampaniaPrograma
        fields = ("costo_asignado", "unidad_academica", "campania", "programa")
       
    def get_programa(self, obj):
        return f"{obj.programa.nombre}" if obj.programa else None
    
    def get_campania(self, obj):
        return f"{obj.campania.nombre}" if obj.campania else None   
    
class InscripcionSerializer(serializers.ModelSerializer):
    pagos = serializers.SerializerMethodField()
    estudiante_r = serializers.SerializerMethodField()
    campania_programa_r = serializers.SerializerMethodField()
    
    # Campos para precios personalizados (opcionales)
    tiene_precio_custom = serializers.BooleanField(required=False, default=False)
    costo_inscripcion_acordado = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False, 
        allow_null=True
    )
    costo_mensualidad_acordado = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False, 
        allow_null=True
    )
    costo_documentacion_acordado = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False, 
        allow_null=True
    )
    notas_precio_custom = serializers.CharField(
        required=False, 
        allow_blank=True, 
        allow_null=True
    )
    
    class Meta:
        model = Inscripcion
        fields = (
            'id', 'fecha_inscripcion', 'estudiante', 'campania_programa', 
            'pagos', 'estudiante_r', 'campania_programa_r',
            'tiene_precio_custom', 'costo_inscripcion_acordado', 
            'costo_mensualidad_acordado', 'costo_documentacion_acordado',
            'notas_precio_custom', 'notas_precio_custom'
        )
        read_only_fields = [
            "estudiante", "campania_programa", "pagos", 
            'estudiante_r', 'campania_programa_r'
        ]
    
    @transaction.atomic 
    def create(self, validated_data):        
        return super().create(validated_data)

    def get_pagos(self, obj):
        from myapps.control_escolar.serializer import PagoSerializer
        return PagoSerializer(obj.pagos.all(), many=True).data
    
    def get_estudiante_r(self, obj):
        estudiante = getattr(obj, "estudiante", None)
        if estudiante is None:
            return None
        return EstudianteSerializer(estudiante, many=False).data
    
    def get_campania_programa_r(self, obj):
        cp = getattr(obj, "campania_programa", None)
        if not cp:
            return None
        return CamapaniaSerializer(cp, many=False).data
    
    
class InscripcionDetalleSerializer(serializers.ModelSerializer):
    pagos = serializers.SerializerMethodField()
    pagos_completados = serializers.SerializerMethodField()
    campania_programa_r = serializers.SerializerMethodField()
    total_pagado = serializers.DecimalField(
        source='total_pagado_calc',
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    saldo_pendiente = serializers.DecimalField(
        source='saldo_pendiente_calc',
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    # Campos de precios personalizados
    tiene_precio_custom = serializers.BooleanField(read_only=True)
    costo_inscripcion_acordado = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True,
        allow_null=True
    )
    costo_mensualidad_acordado = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True,
        allow_null=True
    )
    costo_documentacion_acordado = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True,
        allow_null=True
    )
    notas_precio_custom = serializers.CharField(read_only=True, allow_null=True)
    
    class Meta:
        model = Inscripcion
        fields = (
            'id', 'fecha_inscripcion', 'campania_programa_r', 'pagos', 'pagos_completados',
            'estado', 'total_pagado', 'saldo_pendiente',
            'tiene_precio_custom', 'costo_inscripcion_acordado',
            'costo_mensualidad_acordado', 'costo_documentacion_acordado',
            'notas_precio_custom'
        )
    
    def get_pagos(self, obj):
        from myapps.control_escolar.serializer import PagoSerializer
        pagos = obj.pagos.exclude(estado="completado")
        return PagoSerializer(pagos, many=True).data
    
    def get_pagos_completados(self, obj):
        from myapps.control_escolar.serializer import PagoSerializer
        pagos = obj.pagos.filter(estado="completado")
        return PagoSerializer(pagos, many=True).data
    
    def get_campania_programa_r(self, obj):
        cp = getattr(obj, "campania_programa", None)
        if not cp:
            return None
        return CamapaniaSerializer(cp, many=False).data


class EstudianteConInscripcionesSerializer(serializers.ModelSerializer):
    # especialidad = serializers.CharField(source='especialiadad.nombre', read_only=True)
    lugar_nacimiento = serializers.CharField(source='lugar_nacimiento.nombre', read_only=True)
    municipio = serializers.CharField(source='municipio.nombre', read_only=True)
    perfil = serializers.SerializerMethodField(read_only=True)
    inscripciones = serializers.SerializerMethodField()
    total_inscripciones = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = [
            "id", "curp", "rfc", "especialidad", "lugar_nacimiento", 
            "direccion", "activo", "perfil", "municipio",
            "total_inscripciones", "inscripciones"
        ]
    
    def get_perfil(self, obj):
        return f"{obj.perfil.nombre} {obj.perfil.apellidoP} {obj.perfil.apellidoM}"
    
    def get_inscripciones(self, obj):
        # Obtener todas las inscripciones del estudiante
        inscripciones = obj.inscripcion.all()
        return InscripcionDetalleSerializer(inscripciones, many=True).data