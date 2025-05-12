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
    class Meta:
        model = Campania
        fields = '__all__'
        
        
class CampaniaProgramaSerializer(serializers.ModelSerializer):
    campania = CampaniaSerializer()
    programa = ProgramaEducativoSerializer()
    class Meta:
        model = CampaniaPrograma
        fields = ["id", "campania", "programa", "costo_asignado"]