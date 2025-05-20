from django.urls import path, re_path
from .views import (
    TeacherView, TeacherReadView, TeacherEditView
)

urlpatterns = [
    path("teacher/create/", TeacherView.as_view(), name="post"),
    path("teachers/all/", TeacherView.as_view(), name="get"),
    path("teacher/<int:id>/", TeacherReadView.as_view(), name="get"),
    path("teacher/edit/<int:id>/", TeacherEditView.as_view(), name="get"),
    path("teacher/update/<int:id>", TeacherEditView.as_view(), name="patch")
]
