from myapps.authentication.models import UserCustomize, Roles, Permissions
from rest_framework import serializers
from myapps.perfil.models import Profile
from myapps.perfil.serializers import ProfileSerializer
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from myapps.cursos.models import (
    Category,
    SubCategory,
    Especification,
    EducationalProgram,
)
from django.db import transaction


class EspecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especification
        fields = ["id", "name", "subcategory"]

    def create(self, validated_data):
        subca = validated_data.pop("subcategory", None)
        esp = Especification.objects.create(**validated_data)
        if subca:
            esp.subcategory = subca
            esp.save()
        return esp

    def update(self, instance, validated_data):
        subcategory = validated_data.pop("subcategory")
        # print(type(subcategory))
        instance.name = validated_data["name"]
        instance.subcategory = subcategory
        instance.save()
        return instance

    def update_especifications(self, subcategory, especifications):
        try:
            with transaction.atomic():
                especifications_existend = Especification.objects.filter(
                    subcategory=subcategory.id
                )
                new_names = set(especifications)
                # print(especifications_existend, new_names)
                if not especifications_existend:
                    newEspec = [
                        Especification(name=name, subcategory=subcategory)
                        for name in new_names
                    ]
                    if newEspec:
                        Especification.objects.bulk_create(newEspec)
                        return True

                actual_names = set(
                    especifications_existend.values_list("name", flat=True)
                )
                esp_to_delete = especifications_existend.exclude(name__in=new_names)
                esp_to_delete.delete()
                to_create = new_names - actual_names
                # print(esp_to_delete)
                updateEsp = [
                    Especification(name=name, subcategory=subcategory)
                    for name in to_create
                ]
                if updateEsp:
                    Especification.objects.bulk_create(updateEsp)
                return True
                # especification = Especification.objects.bulk_create(especifications)
                # print(subcategory)
        except Exception as e:
            raise serializers.ValidationError(
                f"Error al actualizar especificaciones: {str(e)}"
            )


class SubCategorySerializer(serializers.ModelSerializer):
    especification = EspecificationSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = SubCategory
        fields = ["id", "name", "category", "especification"]

    def create(self, validated_data):
        category = validated_data.pop("category", None)
        sub_category = SubCategory.objects.create(**validated_data)
        if category:
            sub_category.category = category
            sub_category.save()
        return sub_category

    def update(self, instance, validated_data):
        # print(instance.name)
        category = validated_data.pop("category", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.category = category
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=True, required=False, read_only=True)
    # subcategory_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "subcategory"]

    def validate(self, attrs):
        # c = Category.objects.filter(name=attrs["name"])
        # if c.exists():
        #     raise serializers.ValidationError(
        #         {"name": "Ya existe una categoría con este nombre."}
        #     )
        # elif self.instance is not None:
        #     existing = existing.exclude(pk=self.instance.pk)
        # return attrs
        existing = Category.objects.filter(name=attrs["name"])
        if self.instance is not None:
            existing = existing.exclude(pk=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError(
                {"name": "Ya existe una categoría con este nombre."}
            )
        return attrs

    def create(self, validated_data):
        # print(valideted_data)
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        # print(instance.name, validated_data.get("name", instance.name))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    # def many_categorys(self, ):

    # revisar
    # def update(self, instance, validated_data):
    #     # Actualizar todos los campos que vengan en validated_data
    #     # print(instance)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance


class EducationalProgramSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    subcategory = SubCategorySerializer(required=True)
    specification = EspecificationSerializer(required=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    hour_start = serializers.TimeField(required=False, allow_null=True)
    hour_end = serializers.TimeField(required=False, allow_null=True)
    duration = serializers.IntegerField(required=False, allow_null=True)
    price = serializers.DecimalField(
        required=False, allow_null=True, max_digits=10, decimal_places=2, default=0.00
    )
    max_capacity = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = EducationalProgram
        fields = "__all__"

    def create(self, validated_data):
        try:
            with transaction.atomic():
                category = validated_data.pop("category", None)
                subcategory = validated_data.pop("subcategory", None)
                specification = validated_data.pop("specification", None)
                education_program = EducationalProgram.objects.create(**validated_data)
                c = Category.objects.get(id=category)
                s = SubCategory.objects.get(id=subcategory)
                spe = Especification.objects.get(id=specification)
                education_program.category = c
                education_program.subcategory = s
                education_program.specification = spe
                education_program.save()
                return education_program
        except Exception as e:
            raise serializers.ValidationError(
                f"Error al crear el programa educacional: {str(e)}"
            )
