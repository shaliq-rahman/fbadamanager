from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from adminconsole.views import  account, dashboard, masters

app_name = 'adminconsole'

urlpatterns = [
    path('', dashboard.HomeView.as_view(), name='dashboard'),
    path('login/', account.Login.as_view(), name='login'),
    path('logout/', account.Logout.as_view(), name='logout'),
    path('profile/', account.Profile.as_view(), name='profile'),
    
    #DASHBOARD
    path('dashboard/', dashboard.Dashboard.as_view(), name='dashboard'),
    
    #BANNER
    path('users/', masters.UserView.as_view(), name='users'),
    path('user/add/', masters.UserCreateView.as_view(), name='create_user'),
    path('user/<str:id>/update/', masters.UserUpdateView.as_view(), name='update_user'),
    path('user/<str:id>/toggle/', masters.UserToggleView.as_view(), name='toggle_user'),
    path('user/<str:id>/delete/', masters.UserDeleteView.as_view(), name='delete_user'),
    
]