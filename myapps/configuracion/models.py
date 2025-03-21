from django.db import models

# Create your models here.


class MenuItems(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=50)
    itemCount = models.IntegerField()
    bgColor = models.CharField(max_length=20)
    textColor = models.CharField(max_length=20)
    
    # Posterior ver tema de permisos y roles