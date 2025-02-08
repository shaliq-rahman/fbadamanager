from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

def facebook(request):
    # Replace with your access token, app id, and app secret
    ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
    APP_ID = '1124273585947713'
    APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
    AD_ACCOUNT_ID = '978087683481395'  # Replace with your Ad Account ID

    # Initialize the API
    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

    # Get the ad account
    ad_account = AdAccount(f'act_{AD_ACCOUNT_ID}')

    # Define campaign fields
    campaign_fields = [
        Campaign.Field.id,
        Campaign.Field.name,
        Campaign.Field.status,
        Campaign.Field.objective,
    ]

    # Fetch campaigns
    campaigns = ad_account.get_campaigns(fields=campaign_fields)

    # Define the fields to fetch for insights
    insights_fields = [
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

    # Define parameters for insights (e.g., date range)
    insights_params = {
        'level': 'ad',  # Fetch data at the ad level
        'date_preset': 'last_7d',  # Data for the last 7 days
        'time_increment': 1,  # Break down metrics daily
    }

    # List to store combined campaign and insights data
    combined_data = []

    # Fetch insights for each campaign
    for campaign in campaigns:
        # Store campaign data
        campaign_data = {
            'id': campaign.get('id'),
            'name': campaign.get('name'),
            'status': campaign.get('status'),
            'objective': campaign.get('objective'),
        }

        # Fetch insights for the campaign
        insights = ad_account.get_insights(fields=insights_fields, params=insights_params)

        # Add insights data to campaign data
        campaign_data['insights'] = [
            {
                field: insight.get(field)
                for field in insights_fields
            }
            for insight in insights
        ]

        # Append campaign data with insights to the combined data list
        combined_data.append(campaign_data)

    return combined_data
