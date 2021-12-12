import yaml

### read the config
yaml_file = 'config.yml'
try:
    with open(yaml_file, 'r') as c_file:
        config = yaml.safe_load(c_file)
except Exception as e:
    print('Error reading the config file')

def logs_dir():
    return config['directories']['logs_dir']

def racebest_base_url():
    return config['urls']['racebest_base_url']

def racebest_headers_shelve():
    return config["shelves"]["racebest_headers"]