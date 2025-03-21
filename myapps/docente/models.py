from django.db import models
from myapps.authentication.models import UserCustomize
from django.db.models.fields.related import ForeignKey
# Create your models here.

class Teacher(models.Model):
    user =  models.ForeignKey(UserCustomize, on_delete=models.CASCADE, null=True)
    # especializacion
    # cv
    # ver otros campos mas ...