from django.db import models
from myapps.crm.model import Base

class BaseModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=50)
    

class Country(Base, BaseModel):
    country_code = models.CharField(max_length=10, null=True, blank=True)

class City(Base, BaseModel):
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.CASCADE)
    
