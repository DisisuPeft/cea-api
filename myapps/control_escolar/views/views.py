from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from myapps.perfil.models import User
from myapps.perfil.serializer import ProfileSerializer
from myapps.authentication.authenticate import CustomJWTAuthentication
# from myapps.perfil.models import (NivelEducativo, Genero)
# from myapps.perfil.serializer import (NivelEducativoSerializer)
# from myapps.authentication.models import (Roles)
# Create your views here.


# class NivelesEducativos(APIView):
#     authentication_classes = [CustomJWTAuthentication]
#     permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         niveles = NivelEducativo.objects.all()
#         if not niveles:
#             return Response("No existen niveles educativos", status=status.HTTP_404_NOT_FOUND)
#         serializer = NivelEducativoSerializer(niveles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        