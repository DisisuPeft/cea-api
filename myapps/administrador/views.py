from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from myapps.perfil.models import Profile
from myapps.perfil.serializers import ProfileSerializer
from myapps.authentication.authenticate import CustomJWTAuthentication

class UsuariosAdministrador(APIView):
    permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "El usuario no se encuentra autenticado"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
        usuarios = UserCustomize.objects.exclude(email=user.email)
    
        if not usuarios.exists():
            return Response(
                "No existen usuarios", 
                status=status.HTTP_404_NOT_FOUND
            )
    
        serializer = UserCustomizeSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
    
    def post(self, request, *args, **kwargs):
        # print(request.data)
        role = [int(roles) for roles in request.data['role']]
        user_dict = {}
        perfil_dict = {}
        user_headers = ['email', 'password']
        perfil_headers = [
            "nombre", "apellidoP", "apellidoM", "edad", 
            "fechaNacimiento", "genero", "nivEdu", "telefono"
        ]

        for i in user_headers:
            if i in request.data and request.data[i]:
                user_dict[i] = request.data[i]
        user_dict['role'] = role
        user_serializer = UserCustomizeSerializer(data=user_dict)
        
        if user_serializer.is_valid():
            user_instance = user_serializer.save()
            for p in perfil_headers:
                if p in request.data and request.data[p]:
                    perfil_dict[p] = request.data[p]
            perfil_dict['user'] = user_instance.id
            # perfil_data = {
            #     'nombre': request.data['nombre'],
            #     'apellidoP': request.data['apellidoP'],
            #     'apellidoM': request.data['apellidoM'], 
            #     'edad': request.data['edad'], 
            #     'fechaNacimiento': request.data['fechaNacimiento'], 
            #     'genero': request.data['genero'], 
            #     'nivEdu': request.data['nivEdu'], 
            #     'telefono':request.data['telefono'],
            #     'user': user_instance.id,
            # }
            # print(user_instance.id)
            perfil_serializer = ProfileSerializer(data=perfil_dict)
            if perfil_serializer.is_valid():
                perfil_serializer.save()
                return Response({"message": "Usuario creado con exito"}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
        # print(user_dict)
        # return Response({"info": "No content"}, status=status.HTTP_204_NO_CONTENT)
        



    def patch(self, request, *args, **kwargs):
        user_id = request.data['id']  
        
        try:
            user = UserCustomize.objects.get(id=user_id)
            profile = user.profile
        except UserCustomize.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # # Preparar datos para actualización
        # user_data = {}
        profile_data = {}
        
        # # Campos de usuario
        if 'email' in request.data and request.data['email']:
            user.email = request.data['email']
        
        if 'password' in request.data and request.data['password']:
            user.set_password(request.data['password'])
        if 'role' in request.data and request.data['role']:
            role = request.data['role']
            separated = role.split(',')
            user.roleID.clear()
            user.roleID.add(*separated)
        
        user.save()
        # if 'role' in request.data and request.data['role']:
        #     user.role = request.data['role']
        
        # # Campos de perfil
        perfil_campos = [
            "nombre", "apellidoP", "apellidoM", "edad", 
            "fechaNacimiento", "genero", "nivEdu", "telefono"
        ]
        
        for campo in perfil_campos:
            # print(campo)
            if campo in request.data and request.data[campo]:
                profile_data[campo] = request.data[campo]
                # if request.data[campo] == 'null':
                #     profile_data[campo] = request.data[campo]
        
        # # Serializers para actualización
        # user_serializer = UserCustomizeSerializer(
        #     user, 
        #     data=user_data, 
        #     partial=True  # Permite actualizaciones parciales
        # )
        profile_serializer = ProfileSerializer(
            profile, 
            data=profile_data, 
            partial=True  
        )   
        try:
        #     # Validar y guardar
            # if user_data:
            #     if user_serializer.is_valid():
            #         user_serializer.save()
            
            if profile_data:
                if profile_serializer.is_valid():
                    profile_serializer.save()
                else:
                    return Response({
                        "error": "Error al actualizar el perfil", 
                        "details": profile_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Usuario editado"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "error": "Error en la actualización", 
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        # email = request.data['email']
        # password = request.data['password']
        # user_serializer = UserCustomizeSerializer(email=email, password=password)
        # if user_serializer.is_valid():
        #     user = user_serializer.save()
        #     perfil_dict = {
        #         "nombre": request.data["nombre"],
        #         "apellidoP": request.data["apellidoP"],
        #         "apellidoM": request.data["apellidoM"],
        #         "edad": request.data["edad"],
        #         "fechaNacimiento": request.data["fechaNacimiento"],
        #         "genero": request.data["genero"],
        #         "nivEdu": request.data["nivEdu"],
        #         "telefono": request.data["telefono"],
        #         "user": user.id
        #     }
        #     profile_serializer = ProfileSerializer(data=perfil_dict)
        #     if profile_serializer.is_valid():
        #         profile_serializer.save()
        #         return Response({"message":"Usuario editado"}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({"error":"Error al actualizar el usuario"}, status=status.HTTP_400_BAD_REQUEST)

# class EditUsers(APIView):
#     permission_classes = [HasRoleWithRoles(["Administrador"]),  IsAuthenticated]
#     def patch(self, request, *args, **kwargs):
#         email = request.data['email']
#         password = request.data['password']
#         user_serializer = UserCustomizeSerializer(email=email, password=password)
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#             perfil_dict = {
#                 "nombre": request.data["nombre"],
#                 "apellidoP": request.data["apellidoP"],
#                 "apellidoM": request.data["apellidoM"],
#                 "edad": request.data["edad"],
#                 "fechaNacimiento": request.data["fechaNacimiento"],
#                 "genero": request.data["genero"],
#                 "nivEdu": request.data["nivEdu"],
#                 "telefono": request.data["telefono"],
#                 "user": user.id
#             }
#             profile_serializer = ProfileSerializer(data=perfil_dict)
#             if profile_serializer.is_valid():
#                 profile_serializer.save()
#                 return Response({"message":"Usuario editado"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error":"Error al actualizar el usuario"}, status=status.HTTP_400_BAD_REQUEST)
            
    # nombre: "",
    # apellidoP: "",
    # apellidoM: "",
    # edad: null,
    # fechaNacimiento: "",
    # genero: "",
    # nivEdu: "",
    # telefono: "",
    # email: "",
    # password: "",
    # role: null,
        # perfil_dict = {
        #     "nombre": request.data["nombre"],
        #     "apellidoP": request.data["apellidoP"],
        #     "apellidoM": request.data["apellidoM"],
        #     "edad": request.data["edad"],
        #     "fechaNacimiento": request.data["fechaNacimiento"],
        #     "genero": request.data["genero"],
        #     "nivEdu": request.data["nivEdu"],
        #     "telefono": request.data["telefono"],
        # }