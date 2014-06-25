from mws import mws
from jSonCredentials import load_settings

settings = load_settings()

api = mws.Inventory(account_id=settings.AccountID, secret_key=settings.SecretKey,
                    access_key=settings.AccessKey, region='UK')

result = api.list_inventory_supply(skus=('196267', '196268rb'))
pass
