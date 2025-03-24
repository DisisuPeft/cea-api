from django.db import models
from myapps.authentication.models import Roles
# Create your models here.


class MenuItems(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=50)
    itemCount = models.IntegerField()
    bgColor = models.CharField(max_length=20)
    textColor = models.CharField(max_length=20)
    route = models.CharField(max_length=50, null=True, blank=True)
    role = models.ManyToManyField(Roles, related_name='menu_items', null=True, blank=True)
    
    # Posterior ver tema de permisos y roles