from rest_framework import serializers
from myapps.catalogos.models import MetodoPago

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ("id", "nombre")