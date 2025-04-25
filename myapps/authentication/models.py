from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.fields.related import ForeignKey

from myapps.authentication.manager import CustomUserManager
# from myapps.perfil.models import Profile

class Permissions(models.Model):
    name = models.CharField(max_length=10, unique=True)
    
class Roles(models.Model):
    name = models.CharField(max_length=20, unique=True)
    permission = models.ManyToManyField(Permissions, related_name="permissions_role")
    def __str__(self):
        return self.name

class UserCustomize(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    # perfil = models.OneToOneField(Profile, on_delete=models.SET_NULL, related_name='user_customize', null=True)
    roleID = models.ManyToManyField(Roles, related_name='user_customize', null=True, blank=True)
    permission = models.ManyToManyField(Permissions, related_name='permission_user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

# Create your models here.

    def __str__(self):
        return self.email

