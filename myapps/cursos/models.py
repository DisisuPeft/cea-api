from django.db import models
from myapps.docente.models import Teacher
from myapps.authentication.models import UserCustomize


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="subcategory", null=True
    )
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)


class Especification(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, related_name="especification", null=True
    )
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)


class EducationalProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="categorys", null=True
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    hour_start = models.TimeField(null=True, blank=True)
    hour_end = models.TimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name="educationalProgram",
        null=True,
    )
    specification = models.ForeignKey(
        Especification,
        on_delete=models.SET_NULL,
        related_name="educationalProgram",
        null=True,
    )
    # faltaria la inscripcion
    teacher = models.ManyToManyField(
        Teacher,
        related_name="programs",
    )
    status = models.IntegerField(null=True, blank=True)
    tutor = models.ForeignKey(
        UserCustomize, on_delete=models.SET_NULL, related_name="tutor", null=True
    )
    image = models.ImageField(null=True, blank=True)
    # resources = models.ManyToManyField(Resource, related_name="programs")
    # certification = models.BooleanField(default=False)
    # category = models.ForeignKey(
    #     Category,
    #     on_delete=models.SET_NULL,
    #     related_name="category",
    #     null=True,
    # )
class Modulos(models.Model):
    name = models.CharField(max_length=255)
    program = models.ForeignKey(
        EducationalProgram,
        on_delete=models.SET_NULL,
        related_name="educationalProgram",
        null=True,
    )
    
class Lessons(models.Model):
    name = models.CharField(max_length=255)
    modulos = models.ForeignKey(
        Modulos,
        on_delete=models.SET_NULL,
        related_name="educationalProgram",
        null=True,
    )
        