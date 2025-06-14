from rest_framework import serializers
from myapps.catalogos.models import Ciclos, Periodos
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import Evento
from django.utils import timezone
from django.utils.formats import date_format

class CicloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciclos
        fields = ["id", "name", "fecha_inicio", "fecha_fin", "estado"] #0 - sin iniciar // 1 iniciado // 2 finalizado // 99 eliminado
        
        
        def create(self, validated_data):
            try:
                with transaction.atomic():
                    ciclo = Ciclos.objects.create(**validated_data)
                    return ciclo
            except Exception as e:
                raise Exception(f"Rollback database insertion: {e}")
            
            


class EventoSerializer(serializers.ModelSerializer):
    duracion_horas = serializers.SerializerMethodField()
    rango_fechas = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            "id", "nombre", "descripcion", "ciclo", "tipo",
            "fecha_inicio", "fecha_fin", "created_at", "updated_at",
            "duracion_horas", "rango_fechas"
        ]

    def get_duracion_horas(self, obj):
        if obj.fecha_inicio and obj.fecha_fin:
            return round((obj.fecha_fin - obj.fecha_inicio).total_seconds() / 3600, 2)
        return None

    def get_rango_fechas(self, obj):
        if not obj.fecha_fin or obj.fecha_inicio.date() == obj.fecha_fin.date():
            # Evento de un solo día
            return date_format(obj.fecha_inicio, format='DATE_FORMAT')
        else:
            inicio = date_format(obj.fecha_inicio, format='DATE_FORMAT')
            fin = date_format(obj.fecha_fin, format='DATE_FORMAT')
            return f"{inicio} al {fin}"