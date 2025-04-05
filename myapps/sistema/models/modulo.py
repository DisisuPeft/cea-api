from django.db import models
from myapps.authentication.models import Roles
# Create your models here.


class Modulos(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=50)
    bgColor = models.CharField(max_length=20)
    textColor = models.CharField(max_length=20)
    route = models.CharField(max_length=50, null=True, blank=True)
    role = models.ManyToManyField(Roles, related_name='menu_items', null=True, blank=True)