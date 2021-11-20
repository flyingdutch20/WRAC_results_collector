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
logs_dir = config['directories']['logs_dir']
base_url = config['urls']['racebest_base_url']

if not os.path.isdir("./" + logs_dir):
    os.mkdir("./" + logs_dir)
logname = "./" + logs_dir + "/" + date.today().strftime('%Y-%m-%d') + "-results.log"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename=logname,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger("Results.main")
logger.debug('Debug message should go to the log file')
logger.info('Info message to the console and the log file')
logger.warning('Warning message to the console and log file')
logger.error('Error message should go everywhere')

