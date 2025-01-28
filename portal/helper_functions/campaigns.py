from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad

def get_all_campaigns(ad_account_id, access_token):
    """
    Retrieve all campaigns in the specified ad account.
    
    Args:
        ad_account_id (str): The ID of the ad account.
        access_token (str): The access token for the Facebook API.
    
    Returns:
        list: A list of dictionaries containing campaign details.
    """
    FacebookAdsApi.init(access_token=access_token)
    ad_account = AdAccount(ad_account_id)

    # Define fields to retrieve for campaigns
    campaign_fields = [
        'id', 'name', 'status', 'objective', 'bid_strategy', 'daily_budget', 'spend'
    ]

    campaigns = ad_account.get_campaigns(fields=campaign_fields)
    campaign_list = []

    for campaign in campaigns:
        campaign_list.append({
            'campaign_id': campaign['id'],
            'campaign_name': campaign['name'],
            'status': campaign['status'],
            'objective': campaign['objective'],
            'bid_strategy': campaign.get('bid_strategy', 'N/A'),
            'daily_budget': campaign.get('daily_budget', 'N/A'),
            'amount_spent': campaign.get('spend', 'N/A')
        })

    return campaign_list




def get_ad_sets_by_campaign(campaign_id, access_token):
    """
    Retrieve all ad sets for a specific campaign.
    
    Args:
        campaign_id (str): The ID of the campaign.
        access_token (str): The access token for the Facebook API.
    
    Returns:
        list: A list of dictionaries containing ad set details.
    """
    FacebookAdsApi.init(access_token=access_token)
    campaign = Campaign(campaign_id)

    # Define fields to retrieve for ad sets
    adset_fields = [
        'id', 'name', 'status', 'daily_budget', 'bid_strategy', 'spend'
    ]

    ad_sets = campaign.get_ad_sets(fields=adset_fields)
    adset_list = []

    for adset in ad_sets:
        adset_list.append({
            'adset_id': adset['id'],
            'adset_name': adset['name'],
            'status': adset['status'],
            'daily_budget': adset.get('daily_budget', 'N/A'),
            'bid_strategy': adset.get('bid_strategy', 'N/A'),
            'amount_spent': adset.get('spend', 'N/A')
        })

    return adset_list



def get_ads_by_adset(adset_id, access_token):
    """
    Retrieve all ads for a specific ad set and check for post/video links.
    
    Args:
        adset_id (str): The ID of the ad set.
        access_token (str): The access token for the Facebook API.
    
    Returns:
        list: A list of dictionaries containing ad details and insights.
    """
    FacebookAdsApi.init(access_token=access_token)
    adset = AdSet(adset_id)

    # Define fields to retrieve for ads
    ad_fields = [
        'id', 'name', 'status', 'spend', 'creative'
    ]

    # Define metrics to retrieve for insights
    metrics = [
        'impressions', 'cpm', 'ctr', 'cpc', 'clicks',
    ]

    ads = adset.get_ads(fields=ad_fields)
    ad_list = []

    for ad in ads:
        # Check if the ad has a post link or video link
        creative = ad.get('creative', {})
        post_link = creative.get('object_story_spec', {}).get('link_data', {}).get('link', 'N/A')
        video_link = creative.get('object_story_spec', {}).get('video_data', {}).get('video_id', 'N/A')

        # Fetch insights for the ad
        insights = ad.get_insights(fields=metrics)
        insight_data = insights[0] if insights else {}

        ad_list.append({
            'ad_id': ad['id'],
            'ad_name': ad['name'],
            'status': ad['status'],
            'amount_spent': ad.get('spend', 'N/A'),
            'post_link': post_link,
            'video_link': video_link,
            'impressions': insight_data.get('impressions', 'N/A'),
            'cpm': insight_data.get('cpm', 'N/A'),
            'ctr': insight_data.get('ctr', 'N/A'),
            'cpc': insight_data.get('cpc', 'N/A'),
            'clicks': insight_data.get('clicks', 'N/A'),
            'landing_page_views': insight_data.get('landing_page_views', 'N/A'),
            'checkouts_initiated': insight_data.get('checkouts_initiated', 'N/A'),
            'add_to_carts': insight_data.get('add_to_carts', 'N/A'),
            'add_payment_info': insight_data.get('add_payment_info', 'N/A'),
            'cost_per_result': insight_data.get('cost_per_result', 'N/A'),
            'roas': insight_data.get('roas', 'N/A'),
            'video_views': insight_data.get('video_views', 'N/A'),
            'hook_rate': (int(insight_data.get('video_10_sec_watched', 0)) / int(insight_data.get('video_views', 1))) * 100 if insight_data.get('video_views', 0) > 0 else 'N/A',
            'hold_rate': 'N/A'  # Custom logic needed for hold rate
        })

    return ad_list



def get_all_data(ad_account_id, access_token):
    """
    Retrieve all campaigns, ad sets, and ads for the specified ad account.
    
    Args:
        ad_account_id (str): The ID of the ad account.
        access_token (str): The access token for the Facebook API.
    
    Returns:
        dict: A dictionary containing all campaign, ad set, and ad data.
    """
    all_data = {}

    # Retrieve all campaigns
    campaigns = get_all_campaigns(ad_account_id, access_token)
    all_data['campaigns'] = campaigns

    # Retrieve ad sets and ads for each campaign
    for campaign in campaigns:
        campaign_id = campaign['campaign_id']
        ad_sets = get_ad_sets_by_campaign(campaign_id, access_token)
        all_data[campaign_id] = {'ad_sets': ad_sets}

        # Retrieve ads for each ad set
        for adset in ad_sets:
            adset_id = adset['adset_id']
            ads = get_ads_by_adset(adset_id, access_token)
            all_data[campaign_id][adset_id] = {'ads': ads}

    return all_data