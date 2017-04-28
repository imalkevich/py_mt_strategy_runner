""" main.py """

import os
import sys
from datetime import datetime
from util.configuration_parameters import get_configurations
from util.sets import create_set_file
from util.launch import create_ini_file
from util.run_task import exec_commands
from util.start_terminal import init_terminal
from util.terminal import TERMINAL_POOL

SYMBOL = sys.argv[1]
DATE_FROM = sys.argv[2]
DATE_TO = sys.argv[3]

for terminal in TERMINAL_POOL:
    init_terminal(terminal)

configurations = get_configurations()

print("Number of configurations: {}".format(len(configurations)))

command_template = '"{}\\terminal.exe" "{}"'
commands = []
index = 0

for config in configurations:
    terminal_idx = index % len(TERMINAL_POOL)
    terminal_path = TERMINAL_POOL[terminal_idx]
    set_file_name = create_set_file(terminal_path, config, index)
    ini_file = create_ini_file(terminal_path, index, DATE_FROM, DATE_TO, SYMBOL, set_file_name)
    cmd = command_template.format(terminal_path, ini_file)
    commands.append(cmd)
    index = index + 1

start_run = datetime.now()

print("start running terminals {} ...".format(datetime.strftime(start_run, "%b %d %y %H:%M:%S %Z")))

exec_commands(commands, len(TERMINAL_POOL))

finish_run = datetime.now()

print("end running terminals {} ...".format(datetime.strftime(finish_run, "%b %d %y %H:%M:%S %Z")))

input("press Enter to exit ...")