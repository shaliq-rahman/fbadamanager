from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from adminconsole.models import fbAdMetrics

# Replace these with your actual credentials
APP_ID = '1124273585947713'
APP_SECRET = 'aa0eaaede118604c29332769e4910c77'
ACCESS_TOKEN = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
AD_ACCOUNT_ID = 'act_978087683481395'  # Note the "act_" prefix

# Initialize the API
FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)

# ---------------------------
# Step 1: Fetch extended ad details with field expansion
# ---------------------------
# We request the ad's own id and name, plus expand campaign and adset fields,
# and include creative details (image_url and video_id are requested if available).
ad_fields = [
    'id',
    'name',  # This is the ad name.
    'status',
    'campaign{ name, objective }',  # Campaign details including name and objective.
    'adset{ name, daily_budget, bid_strategy }',  # Ad set details.
    'creative{ object_story_spec, image_url, video_id }'  # Creative details.
]

ads = list(AdAccount(AD_ACCOUNT_ID).get_ads(fields=ad_fields))

# Build a dictionary of ad details keyed by ad ID.
ad_details = {}
for ad in ads:
    ad_id = ad.get('id')
    # Campaign details (if available) from field expansion.
    campaign = ad.get('campaign', {})
    campaign_name = campaign.get('name', 'N/A')
    campaign_objective = campaign.get('objective', 'N/A')

    # Ad set details.
    adset = ad.get('adset', {})
    adset_name = adset.get('name', 'N/A')
    daily_budget = adset.get('daily_budget', 'N/A')
    bid_strategy = adset.get('bid_strategy', 'N/A')

    # Ad name and status.
    ad_name = ad.get('name', 'N/A')
    status = ad.get('status', 'N/A')

    # Creative details: Try to detect if it's a video or image creative.
    creative = ad.get('creative', {})
    image_url = creative.get('image_url')
    video_id = creative.get('video_id')
    if video_id:
        # Compose a basic Facebook video URL (this may vary based on your use case)
        creative_link = f"https://www.facebook.com/video.php?v={video_id}"
    elif image_url:
        creative_link = image_url
    else:
        creative_link = 'N/A'

    ad_details[ad_id] = {
        'campaign_name': campaign_name,
        'campaign_objective': campaign_objective,
        'adset_name': adset_name,
        'daily_budget': daily_budget,
        'bid_strategy': bid_strategy,
        'ad_name': ad_name,
        'status': status,
        'creative_link': creative_link
    }

# ---------------------------
# Step 2: Fetch insights metrics using the maximum date preset
# ---------------------------
insight_fields = [
    'ad_id',           # To match insights with the ad details.
    'date_start',      # Earliest date in available period.
    'date_stop',       # Latest date in available period.
    'spend',
    'cpm',
    'cpc',
    'website_ctr',
    'clicks',
    'inline_link_clicks',
    'purchase_roas',   # Return on ad spend (if available)
    'actions'          # Array of action metrics.
]

# Use the "maximum" preset to get up to 37 months of data.
insight_params = {
    'date_preset': 'maximum',
    'level': 'ad'
}

insights = list(AdAccount(AD_ACCOUNT_ID).get_insights(fields=insight_fields, params=insight_params))

# Build a dictionary of insights keyed by ad ID (note: if multiple time slices exist, you may need to aggregate)
insight_details = {}
for record in insights:
    ad_id = record.get('ad_id')
    # Save the first record per ad ID (or you could aggregate if multiple records exist)
    if ad_id not in insight_details:
        insight_details[ad_id] = record

# ---------------------------
# Step 3: Merge data and print results
# ---------------------------
for ad_id, details in ad_details.items():
    insight = insight_details.get(ad_id, {})

    # Retrieve insights values; if not present, mark as "N/A"
    date_start = insight.get('date_start', 'N/A')
    date_stop = insight.get('date_stop', 'N/A')
    spend = insight.get('spend', 'N/A')
    cpm = insight.get('cpm', 'N/A')
    cpc = insight.get('cpc', 'N/A')
    website_ctr = insight.get('website_ctr', 'N/A')
    clicks = insight.get('clicks', 'N/A')
    inline_link_clicks = insight.get('inline_link_clicks', 'N/A')
    purchase_roas = insight.get('purchase_roas', 'N/A')

    # Process the actions array to retrieve conversion-related metrics.
    # Adjust these action types as needed.
    actions = insight.get('actions', [])
    results = 0
    cost_per_result = 'N/A'
    landing_page_views = 'N/A'
    checkouts_initiated = 'N/A'
    add_to_carts = 'N/A'
    add_payment_info = 'N/A'

    for action in actions:
        action_type = action.get('action_type')
        value = float(action.get('value', 0))
        if action_type == 'offsite_conversion.fb_pixel_purchase':
            results += value  # Define "Results" as purchases (adjust if needed)
        elif action_type == 'landing_page_view':
            landing_page_views = value
        elif action_type == 'offsite_conversion.fb_pixel_initiated_checkout':
            checkouts_initiated = value
        elif action_type == 'offsite_conversion.fb_pixel_add_to_cart':
            add_to_carts = value
        elif action_type == 'offsite_conversion.fb_pixel_add_payment_info':
            add_payment_info = value

    # Calculate cost per result if results > 0
    if results:
        try:
            cost_per_result = float(spend) / results
        except Exception:
            cost_per_result = 'N/A'
    else:
        cost_per_result = 'N/A'

    # Hook Rate and Hold Rate are not provided by Facebook;
    # mark them as "N/A" or compute from additional video metrics if available.
    hook_rate = 'N/A'
    hold_rate = 'N/A'

    # Display all details
    print("--------------------------------------------------")
    print("Period/Date:           {} to {}".format(date_start, date_stop))
    print("Campaign Name:         ", details.get('campaign_name'))
    print("Campaign Objective:    ", details.get('campaign_objective'))
    print("Ad Set Name:           ", details.get('adset_name'))
    print("Ad Name:               ", details.get('ad_name'))
    print("Status:                ", details.get('status'))
    print("Bid Strategy:          ", details.get('bid_strategy'))
    print("Daily Budget:          ", details.get('daily_budget'))
    print("Results (Purchases):   ", results)
    print("Cost per Result:       ", cost_per_result)
    print("Amount Spent:          ", spend)
    print("Return on Ad Spend:    ", purchase_roas)
    print("Hook Rate:             ", hook_rate)
    print("Hold Rate:             ", hold_rate)
    print("CPM:                   ", cpm)
    print("Link CTR:              ", website_ctr)
    print("Link CPC:              ", cpc)
    print("Link Clicks:           ", clicks)
    print("Landing Page Views:    ", landing_page_views)
    print("Checkouts Initiated:   ", checkouts_initiated)
    print("Add to Carts:          ", add_to_carts)
    print("Add Payment Info:      ", add_payment_info)
    print("Creative (Video/Image):", details.get('creative_link'))
    print("--------------------------------------------------\n")
    
    ad_metrics, created = fbAdMetrics.objects.update_or_create(
    ad_id=ad_id,
    defaults={
        'period_start': date_start,
        'period_end': date_stop,
        'campaign_name': details.get('campaign_name'),
        'campaign_objective': details.get('campaign_objective'),
        'adset_name': details.get('adset_name'),
        'ad_name': details.get('ad_name'),
        'status': details.get('status'),
        'bid_strategy': details.get('bid_strategy'),
        'daily_budget': details.get('daily_budget'),
        'results': results,
        'cost_per_result': cost_per_result,
        'amount_spent': spend,
        'return_on_ad_spend': purchase_roas,
        'hook_rate': hook_rate,
        'hold_rate': hold_rate,
        'cpm': cpm,
        'link_ctr': website_ctr,
        'link_cpc': cpc,
        'link_clicks': clicks,
        'landing_page_views': landing_page_views,
        'checkouts_initiated': checkouts_initiated,
        'add_to_carts': add_to_carts,
        'add_payment_info': add_payment_info,
        'creative_link': creative_link
    }
    )

    # Check if the instance was created or updated
    if created:
        print("A new instance was created.")
    else:
        print("An existing instance was updated.")