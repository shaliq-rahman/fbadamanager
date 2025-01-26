from django.shortcuts import render
from portal.helper import renderhelper
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from adminconsole.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login  # This imports the correct function
from .utils.campaigns import *
import pdb


#DASHBOARD
class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        data = {}
        return renderhelper(request, "portal", "dashboard", template_name="index.html", context=data)
    
#LOGIN
class LoginView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        return renderhelper(request, "portal", "auth", template_name="login.html", context=data)
    
    def post(self, request, *args, **kwargs):
        username_or_email = request.POST.get('email-username', None)
        password = request.POST.get('password', None)

        if not username_or_email or not password:
            messages.error(request, "Please enter both username (or email) and password.")
            return redirect('portal:login')  # Replace 'login' with the name of your login URL pattern

        # Check if the user exists by email
        user = User.objects.filter(email=username_or_email).first()
        if user:
            username = user.username  # Use the username for authentication
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    # Log the user in
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('portal:dashboard')  # Replace 'dashboard' with the name of your dashboard URL pattern
                else:
                    messages.error(request, "Your account is inactive. Please contact support.")
        else:
            messages.error(request, "Invalid username/email or password.")

        return redirect('portal:login')  # Replace 'login' with the name of your login URL pattern


#CAMPAIGN
class CampaignsView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        
        # Facebook API credentials
        access_token = user.access_token
        app_id = user.app_id
        app_secret = user.app_secret
        ad_account_id = user.ad_account_id
        
        # Initialize the API
        initialize_facebook_api(access_token, app_id, app_secret)
        
        # Fetch campaign data
        campaign_data = fetch_campaign_data(access_token, ad_account_id)
        
        # Pass data to the template
        data = {
            'campaign_data': campaign_data,
        }
        return renderhelper(request, "portal", "campaigns", template_name="index.html", context=data)
    

class CampaignsDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        data = {}
        return renderhelper(request, "portal", "campaigns", template_name="detail.html", context=data)
    
# def myfunction(request):
#     print("Hello this is a test function")

# def login(request):
#     context = {
#         "title": "Example Page",
#         "message": "This is an example of using render_helper."
#     }
#     return renderhelper(request, "portal", "auth", template_name="login.html", context=context)

# def dashboard(request):
#     context = {
#         "title": "Example Page",
#         "message": "This is an example of using render_helper."
#     }
#     return renderhelper(request, "portal", "dashboard", template_name="index.html", context=context)

# def data(request):
#     context = {
#         "title": "Example Page",
#         "message": "This is an example of using render_helper."
#     }
#     return renderhelper(request, "portal", "data_list", template_name="index.html", context=context)


def data_edit(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "data_list", template_name="edit.html", context=context)


def profile_update(request):
    context = {
        "title": "Example Page",
        "message": "This is an example of using render_helper."
    }
    return renderhelper(request, "portal", "profile", template_name="edit.html", context=context)