import logging
from yaml import safe_load

def load_config():
    config = {}
    with open('config.yaml', 'r') as f:
        config = safe_load(f)
    return config

_config = load_config()

dbUrl = _config['dbUrl']
port = _config['port']
logging_format = _config['logging_format']