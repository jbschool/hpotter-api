from yaml import safe_load

def load_config():
    config = {}
    with open('config.yaml', 'r') as f:
        config = safe_load(f)
    return config

config = load_config()

dbUrl = config['dbUrl']
port = config['port']