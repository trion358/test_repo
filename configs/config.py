import json

from os import path


config_path = path.join(path.dirname(__file__), "env_configs.json")


def get_env_configs():
    with open(config_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        config_dict = {
            "credentials": data.get("credentials")
                       }
        return config_dict
