from django.urls import path, re_path
from .views import EducationalProgramView
from .views import CategoryView


urlpatterns = [
    # educationalProgram
    path("educationalprogram/all/", EducationalProgramView.as_view(), name="get"),
    path("educationalprogram/create/", EducationalProgramView.as_view(), name="post"),
    path(
        "educationalprogram/get",
        EducationalProgramView.as_view(),
        name="get_educationalProgram",
    ),
    # categorys
    path("courses/categorys/", CategoryView.as_view(), name="get"),
    path("courses/category/create/", CategoryView.as_view(), name="post"),
    path("courses/category/update/", CategoryView.as_view(), name="patch"),
]
