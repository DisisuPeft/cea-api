from django.utils.decorators import method_decorator  # importante
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.authenticate import CustomJWTAuthentication
from myapps.estudiantes.models import Estudiante
from myapps.sistema.pagination import UsersPagination
from myapps.estudiantes.serializer import EstudianteSerializer
from django.db.models import Q
from myapps.sistema.helpers import normalize_q, tokenize
from myapps.sistema.serializer import PlataformaModuloSerializer
from myapps.control_escolar.models import ProgramaEducativo
from myapps.control_escolar.serializer import ProgramaShowSerializer
from myapps.control_escolar.pagination import ProgramaPagination
from myapps.control_escolar.models import MaterialModulos, TypeFile
from myapps.sistema.serializer import TypeDocumentSerializer, UploadFilesSerializer, MaterialSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from myapps.estudiantes.serializer import UpdateEstudentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import os, mimetypes
from django.http import FileResponse, Http404
from django.conf import settings
from pathlib import Path
from django.http import JsonResponse
from django.views import View
# from myapps.
# Create your views here.

class ManageUsersview(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]), IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        
        user = request.user
        
        q_raw = request.GET.get("q") 
        
        q = (q_raw or "").strip()
        
        if q.lower() in {"null", "undefined", "none", "nan"}:
            q = ""
                
        queryset = (
            Estudiante.objects.exclude(perfil__user_id=user.id).select_related("perfil", "lugar_nacimiento", "municipio").order_by("perfil__nombre", "id")
        )

        if q:
            queryset = queryset.filter(
                Q(perfil__nombre__icontains=q) | Q(perfil__apellidoP__icontains=q) | Q(perfil__apellidoM__icontains=q)
            )
        
  
        paginator = UsersPagination()

        result = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = EstudianteSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        if not request.data:
            return Response("The request is empty", status=status.HTTP_400_BAD_REQUEST)

        estudiante = EstudianteSerializer(data=request.data)
        
        if estudiante.is_valid():
            estudiante.save()
            return Response("Usuario creado con exito", status=status.HTTP_201_CREATED)
        else:
            return Response(estudiante.errors, status=status.HTTP_400_BAD_REQUEST)    
        

class ManageEditUserView(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]), IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, id):
        
        if not id or request.data:
            return Response("id or request empty", status=status.HTTP_400_BAD_REQUEST)
        
        estudiante = Estudiante.objects.get(id=id)
        
        if not estudiante:
            return Response("Estudiante not found", status=status.HTTP_404_NOT_FOUND)
        
        serializer = EstudianteSerializer(estudiante)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        id = request.GET.get("id")
        estudiante = Estudiante.objects.filter(id=id).first()
        
        if not estudiante:
            return Response("El estudiante no existe.", status=status.HTTP_404_NOT_FOUND)

        
        serializer = UpdateEstudentSerializer(instance=estudiante, data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        return Response("Estudiante actualizado con exito.", status=status.HTTP_200_OK)
        


class ManageUserAccessView(APIView):     
    permission_classes = [HasRoleWithRoles(["Administrador"]), IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    
    def post(self, request):
        if not request.data: 
            return Response("The request is empty", status=status.HTTP_400_BAD_REQUEST)
        
        if not request.data["tabmodule"]:
            return Response("No se ha seleccionado un submodulo", status=status.HTTP_400_BAD_REQUEST)

        s = PlataformaModuloSerializer(data=request.data)
        # print(s.is_valid)
        if s.is_valid():
            s.save()
            return Response("Accesos creados", status=status.HTTP_201_CREATED)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)



class ManageDiplomadosview(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]), IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        
        # user = request.user
        
        q_raw = request.GET.get("q") 
        
        q = (q_raw or "").strip()
        
        if q.lower() in {"null", "undefined", "none", "nan"}:
            q = ""
                
        queryset = (
            ProgramaEducativo.objects.filter(activo=1).order_by('-fecha_creacion')
        )

        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q)
            )
        
  
        paginator = ProgramaPagination()

        result = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = ProgramaShowSerializer(result, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    # evitar inscribir dos veces a un estudiante
    def post(self, reuest):
        diplomado_id = reuest.data.pop('curso_id', None)
        estudiante_id = reuest.data.pop('estudiante_id', None)
        
        diplomado = ProgramaEducativo.objects.filter(id=diplomado_id).first()
        
        if diplomado.inscripcion.filter(id=estudiante_id).exists():
            return Response("No puedes inscribir 2 veces al mismo estudiante", status=status.HTTP_400_BAD_REQUEST)
        diplomado.inscripcion.add(estudiante_id)
        
# diplomado.inscripcion.add(estudiante_id)
        # print(exists)
        return Response("Estudiante inscrito", status=status.HTTP_200_OK)



class ManageUploadMaterialDiplomadosview(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]), IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        documents = TypeFile.objects.all()
        if not documents:
            return Response("Error al consultar los tipos de documentos", status=status.HTTP_400_BAD_REQUEST)
        serializer = TypeDocumentSerializer(documents, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # files = request.FILES.get('files')
        modulo_id = request.data.get("moduloId")
        programa_id = request.data.get("programaId")
        type_id = request.data.get("typeId")
        
        files = request.FILES.getlist("files")
        if not files:
            return Response("No se adjuntaron archivos", status=status.HTTP_400_BAD_REQUEST)
        
        created = []
        errors = []
        
        for f in files:
            data = {
                "file": f,
                "modulo": modulo_id,
                "type": type_id,
                "programa": programa_id
            }
            serializer = UploadFilesSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                created.append({
                    "id": instance.id,
                    "file": instance.file.url if instance.file else None
                })
            else: errors.append(serializer.errors)
        
        if errors:
            return Response({"created": created, "errors": errors}, status=400)
        
        return Response("Archivo subido", status=status.HTTP_201_CREATED)  



    
class MaterialViewSet(ModelViewSet):
    queryset = MaterialModulos.objects.all().order_by("-fecha_creacion")
    serializer_class = MaterialSerializer
    permission_classes = [HasRoleWithRoles(["Administrador", "Estudiante"]), IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        programa_id = self.request.query_params.get("programa_id")
        
        if programa_id:
            if hasattr(MaterialModulos, "programa_id"):
                qs = qs.filter(programa_id=programa_id)
        return qs
    
    @action(detail=True, methods=["get"], url_path="download", url_name="download")
    def download(self, request, pk=None):
        mat = self.get_object()
        
        if hasattr(mat.file, "path"):
            abs_path = Path(mat.file.path)
        else:
            abs_path = Path(settings.MEDIA_ROOT) / str(mat.file)
            
        if not abs_path.exists():
            raise Http404("Archivo no encontrado")
        
        filename = abs_path.name
        
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        
        return FileResponse(
            open(abs_path, "rb"),
            as_attachment=True,
            filename=filename,
            content_type=content_type,
        )
        

class DebugProxyView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "scheme": request.scheme,                       # vea “http” o “https”
            "host": request.get_host(),                     # dominio que Django ve
            "forwarded_proto": request.META.get("HTTP_X_FORWARDED_PROTO"),
            "all_headers": {k: v for k, v in request.META.items() if k.startswith("HTTP_")},
        })