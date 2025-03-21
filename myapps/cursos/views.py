from django.shortcuts import render
from rest_framework.views import APIView
from myapps.authentication.permissions import HasRoleWithRoles
from myapps.authentication.models import UserCustomize
from myapps.authentication.serializers import UserCustomizeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from myapps.cursos.models import (
    Category,
    SubCategory,
    Especification,
    EducationalProgram,
)
from myapps.cursos.serializers import (
    CategorySerializer,
    SubCategorySerializer,
    EspecificationSerializer,
    EducationalProgramSerializer,
)

# Create your views here.


class EducationalProgramView(APIView):
    permission_classes = [
        IsAuthenticated,
        HasRoleWithRoles(["Administrador", "Docente"]),
    ]

    def get(self, request):
        edu = EducationalProgram.objects.all()
        if not edu:
            return Response(
                {"error": "No existen programas disponibles"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EducationalProgramSerializer(edu, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def get_educationalProgram(self, request):
        ed_id = request.GET.get("id")
        educational = EducationalProgram.objects.get(id=ed_id)
        if not educational:
            return Response(
                {"error": "Este programa educacional no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EducationalProgramSerializer(educational)
        return Response({"program": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EducationalProgramSerializer()
        edprogram = {}
        for row in request.data:
            if (
                row in request.data
                and request.data[row]
                and request.data[row] != "null"
            ):
                edprogram[row] = request.data[row]
        edprogram["status"] = 0
        educational_program = serializer.create(validated_data=edprogram)
        if educational_program:
            pass
        else:
            return Response(
                {"detail": educational_program}, status=status.HTTP_400_BAD_REQUEST
            )
        # print(educationalprogram)
        return Response(
            {"detail": "Recurso creado con exito"}, status=status.HTTP_200_OK
        )


class CategoryView(APIView):
    permission_classes = [
        IsAuthenticated,
        HasRoleWithRoles(["Administrador"]),
    ]  # aca tal vez el rol de tutores academicos

    def get(self, request):
        category = Category.objects.all()
        if not category:
            return Response(
                {"error": "No existen categorias disponibles"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CategorySerializer(category, many=True)
        return Response({"categorys": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        category_serializer = CategorySerializer(
            data={
                "name": request.data["nameCategory"],
                "description": request.data["description"],
            }
        )
        if category_serializer.is_valid():
            category = category_serializer.save()
            # return Response(
            #     {"detail": category},
            #     status=status.HTTP_400_BAD_REQUEST,
            # )
            subcategory = SubCategorySerializer(
                data={
                    "name": request.data["namesubCategory"],
                    "category": category.id,
                }
            )
            if subcategory.is_valid():
                instance_subcategory = subcategory.save()
                if "especification" in request.data and request.data["especification"]:
                    especification = request.data["especification"].split(",")
                    # print(instance_subcategory.id)
                    for row in range(len(especification)):
                        esp_serializer = EspecificationSerializer(
                            data={
                                "name": especification[row],
                                "subcategory": instance_subcategory.id,
                            }
                        )
                        if esp_serializer.is_valid():
                            esp_serializer.save()
            return Response(
                {"detail": "Categoria creada"},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {"detail": category_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request):
        category_id = int(request.query_params.get("category_id"))
        # print(request.data["nameCategory"])
        cat_dict = {}
        subcat_dict = {}
        category = Category.objects.get(id=category_id)
        if not category:
            return Response(
                {"detail": "Categoria no encontrada"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if "nameCategory" in request.data and request.data["nameCategory"]:
            cat_dict["name"] = request.data["nameCategory"]
        if "description" in request.data and request.data["description"]:
            cat_dict["description"] = request.data["description"]
        category_serializer = CategorySerializer(
            category,
            data=cat_dict,
            partial=True,
        )

        if category_serializer.is_valid():
            category_save = category_serializer.save()
            if "namesubCategory" in request.data and request.data["namesubCategory"]:
                subcat_dict["name"] = request.data["namesubCategory"]
                subcat_dict["category"] = category_save.id
                # if "subcategory_id" in request.data and request.data["subcategory_id"]:
                # try:
                subcategory = None
                sub_serializer = None
                if (
                    "subcategory_id" in request.data
                    and request.data["subcategory_id"] != "null"
                ):
                    # print(request.data["subcategory_id"])
                    subcategory = SubCategory.objects.get(
                        id=request.data["subcategory_id"]
                    )
                if subcategory == None:
                    sub_serializer = SubCategorySerializer(data=subcat_dict)
                    if sub_serializer.is_valid():
                        pass
                sub_serializer = SubCategorySerializer(
                    subcategory, data=subcat_dict, partial=True
                )
                if sub_serializer.is_valid():
                    pass
                sub = sub_serializer.save()
                if "especification" in request.data and request.data["especification"]:
                    try:
                        # especification = Especification.objects.filter(
                        #     subcategory=sub.id
                        # )
                        espslice = request.data["especification"].split(",")
                        esp = EspecificationSerializer()
                        result = esp.update_especifications(
                            subcategory=sub,
                            especifications=espslice,
                        )
                        if result:
                            pass
                        else:
                            print(result)
                            return Response(
                                {
                                    "detail": f"Error al actualizar porque el resultado es {result}"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                            # print(esp)
                            # for row in especification:
                            #     for col in range(len(esp)):
                            #         # print(sub.id)
                            #         esp_serializer = EspecificationSerializer(
                            #             row,
                            #             data={
                            #                 "name": esp[col],
                            #                 "subcategory": sub.id,
                            #             },
                            #         )
                            #         if esp_serializer.is_valid():
                            #             esp_serializer.save()

                    except Especification.DoesNotExist:
                        especification = None
                else:
                    return Response(
                        {"detail": sub_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"message": "Categoria editada con exito"},
                status=status.HTTP_200_OK,
            )
            # if "subcategory_id" in request.data and request.data["subcategory_id"]:
            #     try:
            #         subcategory = SubCategory.objects.get(id=request.data["subcategory_id"])
            #     except SubCategory.DoesNotExist:
            #         subcategory = None
            # else:
            #     # Obtener la primera subcategoría de la categoría o None
            #     subcategory = SubCategory.objects.filter(category=category.id).first()
            # if not subcategory:
            #     if (
            #         "namesubCategory" in request.data
            #         and request.data["namesubCategory"]
            #     ):
            #         subcat_dict["name"] = request.data["namesubCategory"]
            #     subcat_dict["category"] = category.id
            #     sub_create = SubCategorySerializer(data=subcat_dict)
            #     if sub_create.is_valid():
            #         subcategory_created = sub_create.save()
            #     else:
            #         return Response(
            #             {"detail": "No se guardaron los cambios"},
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )

            # for s in subca:
            #     for row in range(len(sub)):
            #         subcategory_serializer = SubCategorySerializer(
            #             s, data={"name": sub[row], "category": category.id}
            #         )
            #         if subcategory_serializer.is_valid():
            #             pass
            #         else:
            #             return Response(
            #                 {"detail": subcategory_serializer.errors},
            #                 status=status.HTTP_400_BAD_REQUEST,
            #             )
            # first_subcategory = subca.first()
            # esp_instance = Especification.objects.filter(subcategory=one.id)
            # en este caso porque solo existe una sola subcategoria pero cuando existan mas? en ese caso va a suceder
            # if not esp_instance:
            #     return Response(
            #         {"detail": "Especificacion(es) no encontrada(s)"},
            #         status=status.HTTP_404_NOT_FOUND,
            #     )
            # for row1 in range(len(esp)):
            #     espec = EspecificationSerializer(esp_instance, data={"name": esp[row1]})
            #     if espec.is_valid():
            #         pass
            #     else:
            #         return Response(
            #             {"detail": espec.errors},
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )
            # category_serializer.save()
            # subcategory_serializer.save()
            # espec.save()
        # print(category_serializer.id)
        else:
            return Response(
                {"detail": category_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # especification = request.data["especification"].split(",")
        # # print(instance_subcategory.id)
        # for row in range(len(especification)):
        #     esp = EspecificationSerializer(
        #         data={
        #             "name": especification[row],
        #             "subcategory": instance_subcategory.id,
        #         }
        #     )
        #     if esp.is_valid():
        #         esp.save()
        # return Response(
        #     {"detail": "data"},
        #     status=status.HTTP_200_OK,
        # )
