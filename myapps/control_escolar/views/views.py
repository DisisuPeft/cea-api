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
from myapps.control_escolar.models import ProgramaEducativo
from ..serializer import ProgramaEducativoCatalogSerializer
from ..pagination import ProgramaPagination
# Create your views here.


class GetProgramasCatalogView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    def get(self, request, *args, **kwargs):
        programas = ProgramaEducativo.objects.all().order_by('-fecha_creacion')
        
        paginator = ProgramaPagination()
        
        result = paginator.paginate_queryset(queryset=programas, request=request)
        
        if not programas:
            return Response("No existen programas educativos", status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgramaEducativoCatalogSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
        