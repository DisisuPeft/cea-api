from django.urls import path, re_path
from .views import RetriveTipoProducto


urlpatterns = [
    path('tipo-producto/all/', RetriveTipoProducto.as_view(), name="get")
]