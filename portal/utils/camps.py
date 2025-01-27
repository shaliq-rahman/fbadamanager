from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights

def facebook(request):
    # Replace with your access token, app id, and app secret
    ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
    APP_ID = '1124273585947713'
    APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
    AD_ACCOUNT_ID = 'act_978087683481395'  # Replace with your Ad Account ID

    # Initialize the API
    FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

    # Get campaigns from the ad account
    ad_account = AdAccount(AD_ACCOUNT_ID)
    # Define all campaign fields
    campaign_fields = [
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
        Campaign.Field.pacing_type,
        Campaign.Field.adlabels,
        Campaign.Field.brand_lift_studies,
        Campaign.Field.promoted_object,
        Campaign.Field.special_ad_categories,
        Campaign.Field.special_ad_category,
        Campaign.Field.special_ad_category_country,
        Campaign.Field.execution_options,
        Campaign.Field.topline_id,
    ]

    # Fetch all campaigns for the ad account
    campaigns = ad_account.get_campaigns(fields=campaign_fields)

    # List to store combined campaign and metrics data
    combined_data = []

    # Metrics fields
    metrics_fields = [
        'date_start',                # Date range start
        'date_stop',                 # Date range stop
        'campaign_name',             # Campaign name
        'adset_name',                # Ad set name
        'ad_name',                   # Ad name
        # 'status',                    # Status
        'objective',                 # Objective
        # 'bid_strategy',              # Bid strategy
        # 'results',                   # Results (conversions)
        # 'cost_per_result',           # Cost per result
        # 'daily_budget',              # Daily budget
        'spend',                     # Amount spent
        'purchase_roas',             # Return on ad spend (ROAS)
        'outbound_clicks_ctr',       # Hook rate
        # 'hold_rate',                 # Hold rate (custom metric)
        'cpm',                       # Cost per 1000 impressions
        'ctr',                       # Click-through rate
        'cpc',                       # Cost per click
        # 'link_clicks',               # Link clicks
        # 'landing_page_views',        # Landing page views
        # 'checkouts_initiated',       # Checkouts initiated
        # 'add_to_cart',               # Add to cart
        # 'add_payment_info',          # Add to payment info
    ]

    # Fetch insights for each campaign
    for campaign in campaigns:
        campaign_data = {
            'id': campaign.get('id'),
            'name': campaign.get('name'),
            'status': campaign.get('status'),
            'objective': campaign.get('objective'),
            # Add other campaign fields here if needed
        }

        # Get insights for the current campaign
        insights = campaign.get_insights(
            params={
                'level': 'ad',  # Fetch data at the ad level
                'date_preset': 'last_30d',  # Time range for the insights
                'fields': metrics_fields
            }
        )

        # Append insights data to the campaign data
        campaign_data['insights'] = [
            {
                metric: insight.get(metric)
                for metric in metrics_fields
            }
            for insight in insights
        ]

        # Add the campaign and its insights to the combined data
        combined_data.append(campaign_data)

    return combined_data
