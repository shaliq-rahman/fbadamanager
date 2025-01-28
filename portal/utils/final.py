from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad

# Initialize the API
FacebookAdsApi.init(access_token='EAAPZBhVe4hEEBOZBVkzCVmyX58kmPWZC18JZB3rFttxCWwrAIcicFBHZBI0Qd1iJh6fJwlGjuQQQS6jAF7ZBlSsSPLpj1aFx0VQX1MDtvXDftZAvSEe0ofE0Eh6oaeEUvuZA48VBJZAkBOASPck6TdGGZBCDUcQsllAyoZCLIi128HMfzVZCWo84S9r0HRCQ5gPHh1dS')

# Specify your ad account ID
ad_account_id = 'act_978087683481395'
ad_account = AdAccount(ad_account_id)


# Define the fields and metrics you want to retrieve
campaign_fields = [
    'id', 'name', 'status', 'objective', 'bid_strategy', 'daily_budget', 'spend'
]
adset_fields = [
    'id', 'name', 'status', 'daily_budget', 'bid_strategy', 'spend'
]
ad_fields = [
    'id', 'name', 'status', 'spend'
]
metrics = [
    'impressions', 'cpm', 'ctr', 'cpc', 'clicks'
]

# Fetch campaigns
def getfacebookADS(request):
    campaigns = ad_account.get_campaigns(fields=campaign_fields)

    for campaign in campaigns:
        print(f"Campaign ID: {campaign['id']}")
        print(f"Campaign Name: {campaign['name']}")
        print(f"Status: {campaign['status']}")
        print(f"Objective: {campaign['objective']}")
        # print(f"Bid Strategy: {campaign['bid_strategy']}")
        # print(f"Daily Budget: {campaign['daily_budget']}")
        # print(f"Amount Spent: {campaign['spend']}")

        # Fetch ad sets for the campaign
        adsets = campaign.get_ad_sets(fields=adset_fields)

        for adset in adsets:
            print(f"\tAd Set ID: {adset['id']}")
            print(f"\tAd Set Name: {adset['name']}")
            print(f"\tStatus: {adset['status']}")
            # print(f"\tDaily Budget: {adset['daily_budget']}")
            # print(f"\tBid Strategy: {adset['bid_strategy']}")
            # print(f"\tAmount Spent: {adset['spend']}")

            # Fetch ads for the ad set
            ads = adset.get_ads(fields=ad_fields)

            for ad in ads:
                print(f"\t\tAd ID: {ad['id']}")
                print(f"\t\tAd Name: {ad['name']}")
                print(f"\t\tStatus: {ad['status']}")
                # print(f"\t\tAmount Spent: {ad['spend']}")

                # Fetch insights for the ad
                insights = ad.get_insights(fields=metrics)

                for insight in insights:
                    print(f"\t\t\tImpressions: {insight.get('impressions', 'N/A')}")
                    print(f"\t\t\tCPM: {insight.get('cpm', 'N/A')}")
                    print(f"\t\t\tCTR: {insight.get('ctr', 'N/A')}")
                    print(f"\t\t\tCPC: {insight.get('cpc', 'N/A')}")
                    print(f"\t\t\tClicks: {insight.get('clicks', 'N/A')}")
    