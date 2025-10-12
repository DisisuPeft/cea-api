from django.urls import path, re_path
from .views import (
    LeadsView, LeadView, CreateLeadFromLanding, RecentLeadsView, EstadisticsLeadsView, PipelineAllView, GetEmpresaView, GetProgramsView, GetUnidadAcademicaView, PipelineUpdateView,
    GetFuentesView, GetEstatusView, UpdateFuentesView, UpdateEstatusView, GetEtapasPipelineView, GetVendedoresView, CampaniaView, UnidadNegocioView,
)

urlpatterns = [
    path("leads/all/", LeadsView.as_view(), name="get"),
    path("lead/<int:id>/", LeadView.as_view(), name="get"),
    path("registration/lead-landing/", CreateLeadFromLanding.as_view(), name="post"),
    path('recent/leads/', RecentLeadsView.as_view(), name="get"),
    path('leads/estadistics/', EstadisticsLeadsView.as_view(), name="get"),
    path("leads/create/", LeadsView.as_view(), name="post"),
    # pipelines
    path("pipeline/all/", PipelineAllView.as_view(), name="get"),
    path("pipeline/update/<int:id>", PipelineUpdateView.as_view(), name="patch"),
    path('create/pipeline/', PipelineAllView.as_view(), name="post"),
    #crm 
    path("crm/programs/", GetProgramsView.as_view(), name="get"),
    path("crm/unidades-academicas/", GetUnidadAcademicaView.as_view(), name="get"),
    path("crm/empresa/", GetEmpresaView.as_view(), name="get"),
    path("crm/fuentes/", GetFuentesView.as_view(), name="get"),
    path("crm/fuentes/create/", GetFuentesView.as_view(), name="post"),
    path("crm/fuentes/update/<int:id>", UpdateFuentesView.as_view(), name="patch"),
    path('crm/estatus/', GetEstatusView.as_view(), name='get'),
    path("crm/estatus/create/", GetEstatusView.as_view(), name="post"),
    path("crm/estatus/update/<int:id>", UpdateEstatusView.as_view(), name="patch"),
    path("crm/etapas/<int:id>/", GetEtapasPipelineView.as_view(), name="get"),
    path("crm/vendedores/", GetVendedoresView.as_view(), name="get"),
    path('crm/campanias/', CampaniaView.as_view(), name="get"),
    path("crm/unidades/", UnidadNegocioView.as_view(), name="get"),
    

]
