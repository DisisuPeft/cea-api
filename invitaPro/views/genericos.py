from django.shortcuts import render
from myapps.authentication.models import UserCustomize as User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from invitaPro.serializers import TPFormViewSerializar
from invitaPro.models import TipoProducto
# Create your views here.


class RetriveTipoProducto(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        tp = TipoProducto.objects.all()
        if not tp:
            return Response("No hay resultado en la consulta", status=status.HTTP_200_OK)
        serializer = TPFormViewSerializar(tp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
