import json


def load_settings():
    credentials = str(open("credentials.json").read())
    settings_dict = json.loads(credentials, encoding="ASCII")
    str_dict = {}
    for key, val in settings_dict.items():
        if type(key) == unicode:
            key = str(key)
        if type(val) == unicode:
            val = str(val)
        str_dict[key] = val
    return str_dict


class Credentials():
    def __init__(self):
        cred_dict = load_settings()
        self.AccountName = cred_dict['AccountName']
        self.AccountID = cred_dict['AccountID']
        self.MarketplaceID = cred_dict['MarketplaceID']
        self.AccountNumber = cred_dict['AccountNumber']
        self.AccessKey = cred_dict['AccessKey']
        self.SecretKey = cred_dict['SecretKey']
