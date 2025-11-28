from rest_framework import serializers
from myapps.control_escolar.models import Inscripcion, ProgramaEducativo
from myapps.crm.models import CampaniaPrograma

class ProgramaEstudianteSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source="tipo.nombre")
    class Meta:
        model = ProgramaEducativo
        fields = ("nombre", "descripcion", "imagen_url", "id", "tipo")


class InscripcionEstudianteSerializer(serializers.ModelSerializer):
    programa = ProgramaEstudianteSerializer(
        source="campania_programa.programa",
        read_only=True
    )

    class Meta:
        model = Inscripcion
        fields = ("programa",)


        