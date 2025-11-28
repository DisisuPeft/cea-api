from rest_framework import serializers
from myapps.control_escolar.models import TipoPrograma
from myapps.catalogos.models import InstitucionAcademica

class TipoProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPrograma
        fields = ("id", "nombre")