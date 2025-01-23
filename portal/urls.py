from django.urls import path
from .views import *

app_name = 'portal'
urlpatterns = [
    # path('hello/', myfunction, name="myfunction"),
    # path('dashboard/', dashboard, name="dashboard"),
    # path('data/', data, name="data"),
    # path('data-edit/', data_edit, name="data_edit"),
    # path('profile-update/', profile_update, name="profile_update"),
    
    path('', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginView.as_view(), name="login"),
    path('campaigns/', CampaignsView.as_view(), name="campaigns"),
    path('campaigns/<str:id>/detail/', CampaignsDetailView.as_view(), name="campaigns_detail"),
    
]
