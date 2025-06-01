from django.urls import path, re_path
from .views import (
    LeadsView, LeadView, CreateLeadFromLanding, RecentLeadsView, EstadisticsLeadsView, PipelineAllView, GetEmpresaView, GetProgramsView, GetUnidadAcademicaView
)

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("leads/all/", LeadsView.as_view(), name="get"),
    path("lead/<int:id>/", LeadView.as_view(), name="get"),
    path("registration/lead-landing/", CreateLeadFromLanding.as_view(), name="post"),
    path('recent/leads/', RecentLeadsView.as_view(), name="get"),
    path('leads/estadistics/', EstadisticsLeadsView.as_view(), name="get"),
    path("pipeline/all/", PipelineAllView.as_view(), name="get"),\
    path('create/pipeline/', PipelineAllView.as_view(), name="post"),
    path("crm/programs/", GetProgramsView.as_view()),
    path("crm/unidades-academicas/", GetUnidadAcademicaView.as_view()),
    path("crm/empresa/", GetEmpresaView.as_view()),
    # path("logout/", LogoutView.as_view()),
    # # path('auth/user/', ProfileView.as_view()),
    # path("auth/user/", CheckUser.as_view()),
]
