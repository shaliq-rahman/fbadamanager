from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# Replace these with your actual credentials
APP_ID = '1124273585947713'
APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
AD_ACCOUNT_ID = 'act_978087683481395'  # Note the "act_" prefix

# Initialize the API
FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

# Create an instance of your ad account
account = AdAccount(AD_ACCOUNT_ID)

# Define the fields to pull from the ad and insights endpoints.
# Note: Some fields (like campaign_name, adset_name, etc.) are available on the ad object,
# while performance metrics come via the insights endpoint.
fields = [
    # Ad-level details
    'campaign_name',
    'adset_name',
    'ad_name',
    # 'status',
    'objective',
    # 'bid_strategy',
    # 'daily_budget',
    # The insights fields below will be available when using the insights endpoint.
    'date_start',
    'date_stop',
    'spend',
    'cpm',
    'cpc',
    'website_ctr',
    'clicks',
    'inline_link_clicks',
    'actions'  # Contains conversion and other action metrics
]

# Define the parameters for the insights query. Adjust the time_range as needed.
params = {
    'time_range': {'since': '2025-01-01', 'until': '2025-01-31'},
    'level': 'ad'  # Aggregates data at the ad level
}

# Retrieve insights for all ads in the account.
# This call aggregates both ad details and insights in one request.
ads_insights = account.get_insights(fields=fields, params=params)

# Process and print out the details for each ad.
for insight in ads_insights:
    print("--------------------------------------------------")
    print("Campaign Name: ", insight.get('campaign_name'))
    print("Ad Set Name:   ", insight.get('adset_name'))
    print("Ad Name:       ", insight.get('ad_name'))
    # print("Status:        ", insight.get('status'))
    print("Objective:     ", insight.get('objective'))
    # print("Bid Strategy:  ", insight.get('bid_strategy'))
    # print("Daily Budget:  ", insight.get('daily_budget'))
    print("Date Range:    {} to {}".format(insight.get('date_start'), insight.get('date_stop')))
    print("Amount Spent:  ", insight.get('spend'))
    print("CPM:           ", insight.get('cpm'))
    print("Link CPC:      ", insight.get('cpc'))
    print("Link CTR:      ", insight.get('website_ctr'))
    print("Clicks:        ", insight.get('clicks'))
    print("Link Clicks:   ", insight.get('inline_link_clicks'))

    # Process conversion actions.
    actions = insight.get('actions', [])
    if actions:
        for action in actions:
            action_type = action.get('action_type')
            value = action.get('value')
            if action_type == 'offsite_conversion.fb_pixel_add_to_cart':
                print("Add to Carts:         ", value)
            elif action_type == 'offsite_conversion.fb_pixel_initiated_checkout':
                print("Checkouts Initiated:  ", value)
            elif action_type == 'offsite_conversion.fb_pixel_add_payment_info':
                print("Add Payment Info:     ", value)
            elif action_type == 'landing_page_view':
                print("Landing Page Views:   ", value)
            # You can add more action types as needed.
    else:
        print("No conversion actions reported.")

    # Note: Metrics such as "Results", "Cost per Result", "Return on Ad Spend", 
    # "Hook Rate", and "Hold Rate" may require additional calculations or custom tracking.
    # For instance, Cost per Result can be computed as (spend / results) if your
    # “results” metric is available or derived from a specific conversion action.
    
    print("--------------------------------------------------\n")
