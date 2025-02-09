from django.urls import path
from .views import *

app_name = 'portal'
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('campaigns/', CampaignsView.as_view(), name="campaigns"),
    path('campaigns/<str:cmpid>/adsets/', CampaignsAdSetsView.as_view(), name="campaigns_adsets"),
    path('campaigns/adsets/<str:adsetid>/ads/', AdView.as_view(), name="campaigns_adsets_ads"),
    path('campaigns/adsets/ads/<str:adid>/insights/', AdInsightsView.as_view(), name="campaigns_ad_insights"),
    path('campaigns/<str:id>/detail/', CampaignsDetailView.as_view(), name="campaigns_detail"),
    
    path('ads/', CampaignsAdsView.as_view(), name="campaign_ads"),
    path('ads/<str:adid>/', CampaignsAdsDetailView.as_view(), name="campaign_ads_detail"),
    
    path('download-excel/', download_excel, name='download_excel'),
    path('fetch-latest-ads/', fetch_latest_ads, name='fetch_latest_ads'),
]
