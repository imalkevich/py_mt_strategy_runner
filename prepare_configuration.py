""" prepare configuration """

import sys
from datetime import datetime
from db.configuration import get_configuration_by_name
from db.configuration_option import insert_configuration, get_configurations_count
from util.configuration_parameters import get_configurations

start_run = datetime.now()
print("start preparing configurations {} ...".format(datetime.strftime(start_run, "%b %d %y %H:%M:%S %Z")))

count = get_configurations_count()

print("Configurations count: {}".format(count))

CONFIGURATION_TAG = sys.argv[1]

if not CONFIGURATION_TAG:
    raise ValueError("Configuration tag should be specified.")

configuration = get_configuration_by_name(CONFIGURATION_TAG)

if not configuration:
    raise ValueError("Unable to find configuration by name: {}".format(CONFIGURATION_TAG))

configurations = get_configurations()

print("Number of configurations: {}".format(len(configurations)))

for config in configurations:
    insert_configuration(config, configuration['ConfigurationId'])

finish_run = datetime.now()
print("end preparing configurations {} ...".format(datetime.strftime(finish_run, "%b %d %y %H:%M:%S %Z")))

input("press Enter to exit ...")
