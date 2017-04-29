""" prepare configuration """

from datetime import datetime
from db.configuration_option import insert_configuration, get_configurations_count
from util.configuration_parameters import get_configurations

start_run = datetime.now()
print("start preparing configurations {} ...".format(datetime.strftime(start_run, "%b %d %y %H:%M:%S %Z")))

count = get_configurations_count()

print("Configurations count: {}".format(count))

configurations = get_configurations()

print("Number of configurations: {}".format(len(configurations)))

for config in configurations:
    insert_configuration(config)

finish_run = datetime.now()
print("end preparing configurations {} ...".format(datetime.strftime(finish_run, "%b %d %y %H:%M:%S %Z")))

input("press Enter to exit ...")
