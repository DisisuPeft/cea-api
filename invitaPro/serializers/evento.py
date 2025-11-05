from rest_framework import serializers
from invitaPro.models import Evento, TipoProducto, ItinerarioPaso


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ["id", "name", "slug", "precio_venta", "fecha_contrato"]
        
        
class ItinerarioPasoSerializer(serializers.ModelSerializer):
    # evento_slug = serializers.SerializerMethodField()
    hour = serializers.TimeField(format="%H:%M")
    class Meta:
        model = ItinerarioPaso
        fields = [
            "id",
            "titulo",
            "orden",
            "release_at",
            "offset_minutes",
            "paso",
            "url_map",
            "password_match",
            "hour",
            "descripcion"
        ]
        
