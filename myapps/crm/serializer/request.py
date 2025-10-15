from rest_framework import serializers
from ..models import Request


# from myapps.sistema.serializer import

class RequestSerializer(serializers.ModelSerializer):
    fuente = serializers.SerializerMethodField(required=False)
    tiempo_primera_respuesta = serializers.SerializerMethodField(required=False)
    interesado_en = serializers.SerializerMethodField(required=False)
    producto_interes = serializers.SerializerMethodField(required=False)
    empresa = serializers.SerializerMethodField(required=False)
    city = serializers.SerializerMethodField(required=False)
    
    class Meta:
        model=Request
        fields=["id", "nombre", "correo", "telefono", "fuente", "interesado_en", "producto_interes", "empresa", "city", "tiempo_primera_respuesta"]
        
    def get_fuente(self, obj):
        return obj.fuente.nombre if obj.fuente else None
    
    def get_tiempo_primera_respuesta(self, obj):
        duration = obj.tiempo_primera_respuesta
        total_seconds = int(duration.total_seconds())
        seconds = abs(int(total_seconds))
        
        # operations
        
        days = seconds // 86400
        horas = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        segundos = seconds % 60
        
        if days >= 1:
            format_date = f"{days} día(s), {horas:02}:{minutes:02}:{segundos:02}"
        if days == 0:
            format_date = f"{horas:02}:{minutes:02}:{segundos:02}"
            
        return format_date if obj.tiempo_primera_respuesta else None
    
    def get_interesado_en(self, obj):
        return obj.interesado_en.nombre if obj.interesado_en else None
    
    def get_producto_interes(self, obj):
        return obj.producto_interes.name if obj.producto_interes else None
    
    def get_empresa(self, obj):
        return obj.empresa.nombre if obj.empresa else None
    
    def get_city(self, obj):
        return obj.city.nombre if obj.city else None