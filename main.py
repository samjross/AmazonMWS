from mws import mws
from jSonCredentials import Credentials

credentials = Credentials()

# api = mws.Inventory(account_id=credentials.AccountID, secret_key=credentials.SecretKey,
# access_key=credentials.AccessKey, region='UK')
#
# result = api.list_inventory_supply(skus=('FBAFBA_110919', '196268rb'))

api = mws.Reports(access_key=credentials.AccessKey, secret_key=credentials.SecretKey,
                  account_id=credentials.AccountID, region='UK')

x = api.request_report(report_type='_GET_FLAT_FILE_OPEN_LISTINGS_DATA_',
                       marketplaceids=(credentials.MarketplaceID,))
