from mws import mws
from jSonCredentials import Credentials

credentials = Credentials()

# api = mws.Inventory(account_id=credentials.AccountID, secret_key=credentials.SecretKey,
# access_key=credentials.AccessKey, region='UK')
#
# result = api.list_inventory_supply(skus=('FBAFBA_110919', '196268rb'))

api = mws.Reports(access_key=credentials.AccessKey, secret_key=credentials.SecretKey,
                  account_id=credentials.AccountID, region='UK')

# request = api.request_report(report_type='_GET_FLAT_FILE_OPEN_LISTINGS_DATA_',
#                      marketplaceids=(credentials.MarketplaceID,))

request_list = api.get_report_request_list()
# what I'm going to need to do is, when I make a request I need to store the report ID.
# Then, I check every now and then if that report ID is 'done'
# if it is, use api.get_report(reportID) to get the report
# will see what happens after that...
