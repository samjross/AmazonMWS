from mws import mws
from jSonCredentials import Credentials

credentials = Credentials()

api = mws.Inventory(account_id=credentials.AccountID, secret_key=credentials.SecretKey,
                    access_key=credentials.AccessKey, region='UK')

result = api.list_inventory_supply(skus=('196267', '196268rb'))
