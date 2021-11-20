import os
import logging
import yaml

import result


yaml_file = 'config.yml'
try:
    with open(yaml_file, 'r') as c_file:
      config = yaml.safe_load(c_file)
except Exception as e:
    print('Error reading the config file')
base_url = config['urls']['racebest_base_url']

logger = logging.getLogger("Results.racebest")

