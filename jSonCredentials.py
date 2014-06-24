import json

def load_settings():
    credentials = str(open("credentials.json").read())
    print(credentials)
    settings_object = json.loads(credentials, encoding="ASCII")
    ret_dict = {}
    for key, val in settings_object.items():
        if type(key) == unicode:
            key = str(key)
        if type(val) == unicode:
            val = str(val)
        ret_dict[key] = val
    return ret_dict
