from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from adminconsole.models import fbAdMetrics

app_id = '1124273585947713'
app_secret = 'aa0eaaede118604c29332769e4910c77'
access_token = 'EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS'
ad_account_id = 'act_978087683481395'  # Note the "act_" prefix

import pdb

def fetch_facebook_ad_metrics():
    """Fetch ad metrics from Facebook and update the database."""
    
    # Initialize the API
    FacebookAdsApi.init(app_id, app_secret, access_token)
    
    # Fetch extended ad details
    ad_fields = [
        'id', 'name', 'status',
        'campaign{ name, objective }',
        'adset{ name, daily_budget, bid_strategy }',
        'creative{ object_story_spec, image_url, video_id }'
    ]
    
    ads = list(AdAccount(ad_account_id).get_ads(fields=ad_fields))
    
    ad_details = {}
    for ad in ads:
        ad_id = ad.get('id')
        campaign = ad.get('campaign', {})
        adset = ad.get('adset', {})
        creative = ad.get('creative', {})
        
        ad_details[ad_id] = {
            'campaign_name': campaign.get('name', 'N/A'),
            'campaign_objective': campaign.get('objective', 'N/A'),
            'adset_name': adset.get('name', 'N/A'),
            'daily_budget': adset.get('daily_budget', 'N/A'),
            'bid_strategy': adset.get('bid_strategy', 'N/A'),
            'ad_name': ad.get('name', 'N/A'),
            'status': ad.get('status', 'N/A'),
            'creative_link': f"https://www.facebook.com/video.php?v={creative['video_id']}" 
                if 'video_id' in creative else creative.get('image_url', 'N/A')
        }
    
    # Fetch insights metrics
    insight_fields = [
        'ad_id', 'date_start', 'date_stop', 'spend', 'cpm', 'cpc',
        'website_ctr', 'clicks', 'inline_link_clicks', 'purchase_roas', 'actions'
    ]
    insight_params = {'date_preset': 'maximum', 'level': 'ad'}
    insights = list(AdAccount(ad_account_id).get_insights(fields=insight_fields, params=insight_params))
    
    insight_details = {record.get('ad_id'): record for record in insights}
    
    # Merge data and update the database
    for ad_id, details in ad_details.items():
        insight = insight_details.get(ad_id, {})
        actions = {action.get('action_type'): float(action.get('value', 0)) for action in insight.get('actions', [])}
        
        results = actions.get('offsite_conversion.fb_pixel_purchase', 0)
        cost_per_result = float(insight.get('spend', 0)) / results if results else 'N/A'
        
        fbAdMetrics.objects.update_or_create(
            ad_id=ad_id,
            defaults={
                'period_start': insight.get('date_start', 'N/A'),
                'period_end': insight.get('date_stop', 'N/A'),
                'campaign_name': details['campaign_name'],
                'campaign_objective': details['campaign_objective'],
                'adset_name': details['adset_name'],
                'ad_name': details['ad_name'],
                'status': details['status'],
                'bid_strategy': details['bid_strategy'],
                'daily_budget': details['daily_budget'],
                'results': results,
                'cost_per_result': cost_per_result,
                'amount_spent': insight.get('spend', 'N/A'),
                'return_on_ad_spend': insight.get('purchase_roas', 'N/A'),
                'cpm': insight.get('cpm', 'N/A'),
                'link_ctr': insight.get('website_ctr', 'N/A'),
                'link_cpc': insight.get('cpc', 'N/A'),
                'link_clicks': insight.get('clicks', 'N/A'),
                'landing_page_views': actions.get('landing_page_view', 'N/A'),
                'checkouts_initiated': actions.get('offsite_conversion.fb_pixel_initiated_checkout', 'N/A'),
                'add_to_carts': actions.get('offsite_conversion.fb_pixel_add_to_cart', 'N/A'),
                'add_payment_info': actions.get('offsite_conversion.fb_pixel_add_payment_info', 'N/A'),
                'creative_link': details['creative_link']
            }
        )
    print("*"*100, "SUCCESS")
    return True