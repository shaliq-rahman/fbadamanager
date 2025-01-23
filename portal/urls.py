from django.urls import path
from .views import *

app_name = 'portal'
urlpatterns = [
    path('hello/', myfunction, name="myfunction"),
    path('login/', login, name="login"),
    path('dashboard/', dashboard, name="dashboard"),
    path('data/', data, name="data"),
    path('data-edit/', data_edit, name="data_edit"),
    path('profile-update/', profile_update, name="profile_update")
]
