from django.urls import path, re_path
from .views import (
    TeacherView
)

urlpatterns = [
    path("teacher/create/", TeacherView.as_view(), name="post"),
    path("teachers/all/", TeacherView.as_view(), name="get"),
    # path("student/<int:id>/", StudentView.as_view(), name="get"),
    # path("student/edit/<int:id>/", StudentUpdateView.as_view(), name="get"),
    # path("student/update/", StudentUpdateView.as_view(), name="patch")
]
