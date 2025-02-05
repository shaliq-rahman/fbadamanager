from django.shortcuts import render
from portal.helper import renderhelper
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from adminconsole.models import User, Campaign, AdSet, Ad, AdMetrics
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login  # This imports the correct function
# from .utils.campaigns import *
# from .utils.camps import *
# from .utils.campaign import *
# from .utils.final import *
from .helper_functions.campaigns import get_all_campaigns, get_ad_sets_by_campaign, get_ads_by_adset
import pdb
from .helper_functions.ads import facebookapicall



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
        app_id = user.app_id
        app_secret = user.app_secret
        access_token = user.access_token
        ad_account_id = f'act_{user.ad_account_id}' 
        
        # # Fetch campaign data
        # campaign_data = get_all_campaigns(ad_account_id, access_token)
        
        # # Iterate over campaign_data to update or create Campaign objects
        # for campaign in campaign_data:
        #     Campaign.objects.update_or_create(
        #         campaign_id=campaign.get('campaign_id', ''),  # Unique identifier
        #         defaults={
        #             'campaign_name': campaign.get('campaign_name', ''),
        #             'status': campaign.get('status', ''),
        #             'objective': campaign.get('objective', ''),
        #             'bid_strategy': campaign.get('bid_strategy'),
        #             'daily_budget': campaign.get('daily_budget', 0),
        #             'amount_spent': campaign.get('amount_spent', 0),
        #             'response_data': campaign.get('response_data', {}),
        #         }
        #     )
            
        campaign_data = Campaign.objects.all()
        data = {
            'campaign_data': campaign_data,
        }
        return renderhelper(request, "portal", "campaigns", template_name="index.html", context=data)
    
    
#ADSETS VIEW
class CampaignsAdSetsView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, cmpid, *args, **kwargs):
        data = {}
        user = User.objects.get(id=request.user.id)
        
        access_token = user.access_token
        ad_account_id = f'act_{user.ad_account_id}' 

        # campaign_id = cmpid
        # campaign = Campaign.objects.get(campaign_id=campaign_id)
        # adsets = get_ad_sets_by_campaign(campaign_id, access_token)
        # for adset in adsets:
        #     AdSet.objects.create(adset_id=adset['adset_id'], 
        #                         adset_name=adset['adset_name'],
        #                         status=adset['status'],
        #                         daily_budget=adset['daily_budget'],
        #                         bid_strategy=adset['bid_strategy'],
        #                         amount_spent=adset['amount_spent'],
        #                         campaign=campaign,
        #                         response_data=adset)
            
        adsets_data = AdSet.objects.all()
        data = {
            'adsets_data': adsets_data,
        }
        return renderhelper(request, "portal", "adsets", template_name="index.html", context=data)
    
#ADVIEW
class AdView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, adsetid, *args, **kwargs):
        data = {}
        user = User.objects.get(id=request.user.id)
        
        access_token = user.access_token
        ad_account_id = f'act_{user.ad_account_id}' 
        
        # adset_id = adsetid
        # adsetmodel = AdSet.objects.get(adset_id=adset_id)
        
        # ad_list = get_ads_by_adset(adset_id, access_token)
        # for ad_data in ad_list:
        #     # Save or update the Ad object
        #     ad, created = Ad.objects.update_or_create(
        #         ad_id=ad_data['ad_id'],
        #         defaults={
        #             'ad_name': ad_data['ad_name'],
        #             'status': ad_data['status'],
        #             'amount_spent': ad_data.get('amount_spent', None) if ad_data.get('amount_spent') != 'N/A' else None,
        #             'post_link': ad_data.get('post_link', None),
        #             'video_link': ad_data.get('video_link', None),
        #             'response_data': ad_data,  # Store the entire response as JSON for reference
        #             'adset': adsetmodel,
        #         }
        #     )
            
        #     # Save or update the AdMetrics object
        #     AdMetrics.objects.update_or_create(
        #         ad=ad,
        #         defaults={
        #             'impressions': ad_data.get('impressions', None) if ad_data.get('impressions') != 'N/A' else None,
        #             'cpm': ad_data.get('cpm', None) if ad_data.get('cpm') != 'N/A' else None,
        #             'ctr': ad_data.get('ctr', None) if ad_data.get('ctr') != 'N/A' else None,
        #             'cpc': ad_data.get('cpc', None) if ad_data.get('cpc') != 'N/A' else None,
        #             'clicks': ad_data.get('clicks', None) if ad_data.get('clicks') != 'N/A' else None,
        #             'landing_page_views': ad_data.get('landing_page_views', None) if ad_data.get('landing_page_views') != 'N/A' else None,
        #             'checkouts_initiated': ad_data.get('checkouts_initiated', None) if ad_data.get('checkouts_initiated') != 'N/A' else None,
        #             'add_to_carts': ad_data.get('add_to_carts', None) if ad_data.get('add_to_carts') != 'N/A' else None,
        #             'add_payment_info': ad_data.get('add_payment_info', None) if ad_data.get('add_payment_info') != 'N/A' else None,
        #             'cost_per_result': ad_data.get('cost_per_result', None) if ad_data.get('cost_per_result') != 'N/A' else None,
        #             'roas': ad_data.get('roas', None) if ad_data.get('roas') != 'N/A' else None,
        #             'video_views': ad_data.get('video_views', None) if ad_data.get('video_views') != 'N/A' else None,
        #             'hook_rate': ad_data.get('hook_rate', None) if ad_data.get('hook_rate') != 'N/A' else None,
        #             'hold_rate': ad_data.get('hold_rate', None) if ad_data.get('hold_rate') != 'N/A' else None,
        #             'response_data': ad_data,  # Store the entire metrics data as JSON for reference
        #         }
        #     )
        
        ads_data = Ad.objects.filter(adset_id=adsetid)
        data = {
            'ads_data': ads_data,
        }
        return renderhelper(request, "portal", "ads", template_name="index.html", context=data)
    
    
class AdInsightsView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request, adid, *args, **kwargs):
        data = {}
        user = User.objects.get(id=request.user.id)
        adinsights = AdMetrics.objects.filter(ad_id=adid)
        data = {
            'adinsights': adinsights,
        }
        return renderhelper(request, "portal", "ads", template_name="detail.html", context=data)
    

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