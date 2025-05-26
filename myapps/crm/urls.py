from django.urls import path, re_path
from .views import (
    LeadsView, LeadView, CreateLeadFromLanding
)

urlpatterns = [
    # re_path(
    #     r'^o/(?P<provider>\S+)/$',
    #     CustomProviderAuthView.as_view(),
    #     name='provider-auth'
    # ),
    path("leads/all/", LeadsView.as_view()),
    path("lead/<int:id>/", LeadView.as_view()),
    path("registration/lead-landing/", CreateLeadFromLanding.as_view(), name="post")
    # path("pipeline/all/", PipelineAllView.as_view()),
    # path("auth/refresh/", CustomTokenRefreshView.as_view()),
    # path("auth/verify/", CustomTokenVerifyView.as_view()),
    # path("auth/register/", RegisterView.as_view()),
    # path("logout/", LogoutView.as_view()),
    # # path('auth/user/', ProfileView.as_view()),
    # path("auth/user/", CheckUser.as_view()),
]
