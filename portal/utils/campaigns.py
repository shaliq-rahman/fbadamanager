from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

def initialize_facebook_api(access_token, app_id, app_secret):
    FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)


def fetch_campaign_data(access_token, ad_account_id):
    # Initialize the API
    FacebookAdsApi.init(access_token=access_token)
    
    # Replace 'act_<ad_account_id>' with your actual Ad Account ID
    ad_account = AdAccount(f'act_{ad_account_id}')
    
    # Define the fields to fetch
    fields = [
    'campaign_id',
    'campaign_name', 
    'adset_name', 
    'ad_name', 
    'objective', 
    'impressions',
    'clicks', 
    'spend',
    'cpm',
    'ctr',
    'cpc',
    'purchase_roas', 
    'actions',
]
    
    # Define parameters (e.g., date range)
    params = {
        'level': 'ad',
        'date_preset': 'last_7d',  # Fetch data for the last 7 days
        'time_increment': 1,      # Break down metrics daily
    }
    
    # Fetch the data
    insights = ad_account.get_insights(fields=fields, params=params)
    return insights
