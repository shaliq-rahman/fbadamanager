from django.shortcuts import render
import pdb

# Create your views here.
def hello(request):
    print("Hello")



from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

def facebook(request):
    # Replace with your access token, app id, and app secret
    ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
    APP_ID = '1124273585947713'
    APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
    AD_ACCOUNT_ID = 'act_978087683481395'  # Replace <your_ad_account_id> with your Ad Account ID

    # Initialize the API
    FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

    # Get campaigns from the ad account
    ad_account = AdAccount(AD_ACCOUNT_ID)
    # Define all campaign fields
    fields = [
        Campaign.Field.id,
        Campaign.Field.account_id,
        Campaign.Field.name,
        Campaign.Field.status,
        Campaign.Field.effective_status,
        Campaign.Field.objective,
        Campaign.Field.buying_type,
        Campaign.Field.created_time,
        Campaign.Field.start_time,
        Campaign.Field.stop_time,
        Campaign.Field.updated_time,
        Campaign.Field.daily_budget,
        Campaign.Field.lifetime_budget,
        Campaign.Field.spend_cap,
        Campaign.Field.budget_remaining,
        Campaign.Field.bid_strategy,
        # Campaign.Field.optimization_goal,
        Campaign.Field.pacing_type,
        # Campaign.Field.ad_strategy,
        Campaign.Field.adlabels,
        Campaign.Field.brand_lift_studies,
        # Campaign.Field.campaign_group_id,
        Campaign.Field.promoted_object,
        Campaign.Field.special_ad_categories,
        Campaign.Field.special_ad_category,
        Campaign.Field.special_ad_category_country,
        Campaign.Field.execution_options,
        Campaign.Field.topline_id,
    ]

    # Fetch all campaigns for the ad account
    campaigns = ad_account.get_campaigns(fields=fields)
    return campaigns


def facebook_insights(request):
    # Replace with your access token, app id, and app secret
    ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
    APP_ID = '1124273585947713'
    APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
    AD_ACCOUNT_ID = 'act_978087683481395'  # Replace <your_ad_account_id> with your Ad Account ID

    # Initialize the API
    FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

    # Define the fields you want to fetch
    fields = [
        'campaign_name',
        'reach',
        'impressions',
        'spend',
        'clicks',
        # 'cost_per_result',
        'actions',  # Includes conversions like purchases, app installs, etc.
    ]

    # Define parameters for filtering and date range (optional)
    params = {
        'level': 'campaign',  # Fetch insights at the campaign level
        'date_preset': 'last_30d',  # Fetch data for the last 30 days
        'time_increment': 1,  # Daily breakdown (remove if not needed)
    }

    # Fetch insights for the ad account
    ad_account = AdAccount(AD_ACCOUNT_ID)
    insights = ad_account.get_insights(fields=fields, params=params)

    # Print the results
    for insight in insights:
        print("Campaign Insights:")
        for field, value in insight.items():
            print(f"{field}: {value}")
        print("\n" + "="*50 + "\n")  # Separate campaigns for better readability
    pdb.set_trace()
    
    
def get_full_details(request):
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.ad import Ad
    from facebook_business.adobjects.adcreative import AdCreative
    import requests

    ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
    APP_ID = '1124273585947713'
    APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
    AD_ACCOUNT_ID = 'act_978087683481395'  # Replace <your_ad_account_id> with your Ad Account ID

    # Initialize the Facebook API
    FacebookAdsApi.init(app_id=APP_ID, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)

    GRAPH_API_BASE = 'https://graph.facebook.com/v16.0/'

    # Step 1: Fetch Campaigns
    def get_campaigns():
        ad_account = AdAccount(AD_ACCOUNT_ID)
        campaigns = ad_account.get_campaigns(fields=['id', 'name'])
        return campaigns

    # Step 2: Fetch Ad Creatives for a Campaign
    def get_ad_creatives(campaign_id):
        campaign = Campaign(campaign_id)
        ads = campaign.get_ads(fields=['id', 'creative'])
        creative_ids = [ad['creative']['id'] for ad in ads]
        return creative_ids

    # Step 3: Fetch Post Details from Ad Creative
    def get_post_details(creative_id):
        creative = AdCreative(creative_id).api_get(fields=['id', 'object_story_id', 'object_type'])
        post_id = creative.get('object_story_id')

        if not post_id:
            print(f"No post associated with Creative ID: {creative_id}")
            return

        # Fetch post details using Graph API
        post_url = f"{GRAPH_API_BASE}{post_id}?fields=message,created_time,attachments{{media_type,media,url}},comments.summary(true)"
        response = requests.get(post_url, params={'access_token': ACCESS_TOKEN})
        post_details = response.json()

        # Print post details
        print("Post Details:")
        print(f"Message: {post_details.get('message', 'No message')}")
        print(f"Created Time: {post_details.get('created_time')}")
        attachments = post_details.get('attachments', {}).get('data', [])
        for attachment in attachments:
            print(f"Media Type: {attachment.get('media_type')}")
            print(f"Media URL: {attachment.get('media', {}).get('url')}")
        print("\nComments:")
        for comment in post_details.get('comments', {}).get('data', []):
            print(f"- {comment.get('message')}")

    # Main Function to Fetch Campaign Post Details
    def fetch_campaign_post_details():
        campaigns = get_campaigns()
        for campaign in campaigns:
            print(f"Fetching posts for Campaign: {campaign['name']} (ID: {campaign['id']})")
            creative_ids = get_ad_creatives(campaign['id'])
            for creative_id in creative_ids:
                print(f"\nFetching details for Creative ID: {creative_id}")
                get_post_details(creative_id)

    # Run the script
    fetch_campaign_post_details()
    pdb.set_trace()