from mws import mws
from jSonCredentials import Credentials
from flat_file_request import read_amazon_csv

credentials = Credentials()

api = mws.Products(access_key=credentials.AccessKey, secret_key=credentials.SecretKey,
                   account_id=credentials.AccountID, region='UK')

ffile = open('report.txt', 'r')
listings = read_amazon_csv(ffile)
for listing in listings:
    x = api.get_competitive_pricing_for_asin(marketplaceid=credentials.MarketplaceID,
                                             asins=['B00AHGXGIA'])
    pass
