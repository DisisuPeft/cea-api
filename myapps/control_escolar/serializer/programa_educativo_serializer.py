from rest_framework import serializers
from ..models import ProgramaEducativo

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