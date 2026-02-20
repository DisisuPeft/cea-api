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
from myapps.catalogos.models import (InstitucionAcademica)
from myapps.catalogos.serializer import InstitucionSerializarGeneric
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class InstitutosModelViewSet(ModelViewSet):
    queryset = InstitucionAcademica.objects.all()
    serializer_class = InstitucionSerializarGeneric
    permission_classes = [HasRoleWithRoles(["Administrador", "Estudiante", "Tutor"]),  IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get_queryset(self):
        return super().get_queryset()