from rest_framework import serializers
from ..models import ProgramaEducativo, TipoPrograma, ModuloEducativo, SubModulo
from myapps.estudiantes.models import Estudiante
from myapps.perfil.models import User as Profile
from myapps.catalogos.models import InstitucionAcademica

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = ["id", "nombre"]
        


class ProgramaEducativoCatalogSerializer(serializers.ModelSerializer):
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
            'activo',
            'maestro',
            'modalidad',
            'fecha_creacion',
            'fecha_actualizacion',
            'periodo_imparticion',
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
        ]
        
# class TipoProgramaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TipoPrograma
#         fields = ['id']
   
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
    institucion = serializers.SerializerMethodField()
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
            'institucion',
            'duracion_horas',
            'activo',
            'modalidad',
            'costo_inscripcion',
            'costo_mensualidad',
            "inscrito"
        ]
        
    def get_institucion(self, obj):
        return obj.institucion.nombre if obj.institucion else None

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
        