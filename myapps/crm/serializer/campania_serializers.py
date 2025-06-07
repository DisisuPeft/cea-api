from rest_framework import serializers
from ..models import Campania
from myapps.catalogos.serializer import InstitucionAcademicaSerializer
from myapps.catalogos.models import InstitucionAcademica
from .fuentes_serializer import FuenteSerializer
from .estatus_serializer import EstatusSerializer
from .etapas_serializers import EtapaSerializer
from myapps.authentication.serializers import UserCustomizeSerializer
from myapps.catalogos.serializer import InstitucionAcademicaSerializer
from myapps.sistema.serializer import EmpresaSerializer
from ..models.campanias import CampaniaPrograma
from myapps.control_escolar.serializer import ProgramaEducativoSerializer
# from myapps.sistema.serializer import

class CampaniaSerializer(serializers.ModelSerializer):
    programa_campania = serializers.SerializerMethodField()
    class Meta:
        model = Campania
        fields = ["id", "nombre", "descripcion", "fecha_inicio", "fecha_fin", "activa", "programa_campania"]
        
    def get_programa_campania(self, obj):
        return [{"id": p.id, "presupuesto": p.costo_asignado} for p in obj.programa_campania.all()]
    
    
class CampaniaProgramaSerializer(serializers.ModelSerializer):
    campania = serializers.SerializerMethodField()
    programa = serializers.SerializerMethodField()
    class Meta:
        model = CampaniaPrograma
        fields = ["id", "campania", "programa", "costo_asignado"]
        
    def get_campania(self, obj):
        return {"id": obj.campania.id, "nombre": obj.campania.nombre, "fecha_inicio": obj.campania.fecha_inicio, "fecha_fin": obj.campania.fecha_fin} if obj.campania else None

    def get_programa(self, obj):
        return {"id": obj.programa.id, "nombre": obj.programa.nombre} if obj.programa else None