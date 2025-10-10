from django.shortcuts import render
from myapps.authentication.models import UserCustomize as User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from myapps.sistema.models import Empresa
from ..models import Fuentes

# Create your views here.
# EN formularios siempre devolver el puro serializer 

class SaveRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        req = request.data
        return Response(req, status=status.HTTP_200_OK)