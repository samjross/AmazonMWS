import json


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


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
    settings_object = Struct(**str_dict)
    return settings_object
