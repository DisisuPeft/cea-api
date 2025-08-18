from django.urls import path, re_path
from .views.modulos import Modulosview, TabsView, PestaniaEstudianteView
from .views import ManageUsersview

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("menu/all/", Modulosview.as_view(), name="get"),
    path("tabs/all/<int:id>", TabsView.as_view(), name="get"),
    path("plataforma/pestanias/", PestaniaEstudianteView.as_view(), name="get"),

    path("/retrieve-users/", ManageUsersview.as_view(), name="get")
]
