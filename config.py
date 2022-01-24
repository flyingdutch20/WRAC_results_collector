import yaml

def read_yaml_file(yaml_file):
    ### read the config
    try:
        with open(yaml_file, 'r') as c_file:
            return yaml.safe_load(c_file)
    except Exception as e:
        return False

def read_config(yaml_file, param):
    config = read_yaml_file(yaml_file)
    return config[param[0]][param[1]] if config else ''

def logs_dir(yaml_file='config.yml'):
    return read_config(yaml_file,('directories','logs_dir'))

def output_dir(yaml_file='config.yml'):
    return read_config(yaml_file,('directories','output_dir'))

def racebest_base_url(yaml_file='config.yml'):
    return read_config(yaml_file,('urls','racebest_base_url'))

def racebest_headers_shelve(yaml_file='config.yml'):
    return read_config(yaml_file,('shelves','racebest_headers'))

def ukresults_base_url(yaml_file='config.yml'):
    return read_config(yaml_file,('urls','ukresults_base_url'))

def ukresults_headers_shelve(yaml_file='config.yml'):
    return read_config(yaml_file,('shelves','ukresults_headers'))

def runbritain_base_url(yaml_file='config.yml'):
    return read_config(yaml_file,('urls','runbritain_base_url'))

def runbritain_headers_shelve(yaml_file='config.yml'):
    return read_config(yaml_file,('shelves','runbritain_headers'))
