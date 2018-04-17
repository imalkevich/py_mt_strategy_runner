""" main.py """

import os
import sys
import time
from datetime import datetime
from util.sets import create_set_file
from util.launch import create_ini_file
from util.run_task import exec_commands
from util.start_terminal import init_terminal
from util.terminal import TERMINAL_POOL
from util.result_extractor import prepare_results
from db.run import get_by_configuration_id
from db.run_result import get_for_processing_by_run_id, update_run_result_with_report
from db.run_result import remove_run_result_trades_by_configuration_id, reset_run_results_by_configuration_id
from db.configuration_option import get_option_by_id

COMMAND_TEMPLATE = '"{}\\terminal.exe" "{}"'
MAX_WAITS_COUNT = 1

START_TIME = datetime.now()
print("start running terminals {} ...".format(datetime.strftime(START_TIME, "%b %d %y %H:%M:%S %Z")))

CONFIGURATION_ID = int(sys.argv[1])

if len(sys.argv) > 2:
    EXTRA_OPTION = sys.argv[2]
    if EXTRA_OPTION is not None and EXTRA_OPTION == 'refresh':
        remove_run_result_trades_by_configuration_id(CONFIGURATION_ID)
        reset_run_results_by_configuration_id(CONFIGURATION_ID)
        print('reset for configuration {} has been performed...'.format(CONFIGURATION_ID))

RUNS = get_by_configuration_id(CONFIGURATION_ID)
#RUN_NAMES = [name.strip() for name in sys.argv[1].split(",")]

for terminal in TERMINAL_POOL:
    init_terminal(terminal['data_path'])

for run in RUNS:
    run_id = run['RunId']
    run_name = run['Name']
    symbol = run['TestSymbol']
    date_from = run['TestDateFrom']
    date_to = run['TestDateTo']

    number_of_waits = 0

    while True:
        # run batch of commands equal to number of terminals
        commands = []
        results = dict()

        for idx in range(len(TERMINAL_POOL)):
            run_result = get_for_processing_by_run_id(run_id)

            # no configuration for processing
            if run_result is None and len(commands) == 0:
                print("{}: No configuration found for processing... {}"
                      .format(run_name, datetime.strftime(datetime.now(), "%b %d %y %H:%M:%S %Z")))
                time.sleep(0.1) # wait for a while
                number_of_waits = number_of_waits + 1
                if number_of_waits >= MAX_WAITS_COUNT:
                    break
                else:
                    continue
            elif run_result is None:
                break

            config = get_option_by_id(run_result['OptionId'])
            run_result_id = run_result['ResultId']

            terminal_idx = idx % len(TERMINAL_POOL)
            terminal  = TERMINAL_POOL[terminal_idx]
            terminal_path = terminal['exe_path']
            data_path = terminal['data_path']
            set_file_name = create_set_file(data_path, config, run_result_id)
            ini_file = create_ini_file(data_path, run_result_id,
                                       date_from, date_to, symbol, set_file_name)
            cmd = COMMAND_TEMPLATE.format(terminal_path, ini_file)
            commands.append(cmd)

            # for result processing
            results[data_path] = run_result_id

        if number_of_waits >= MAX_WAITS_COUNT:
            print("Stop waiting for configurations to process")
            break

        exec_commands(commands, len(TERMINAL_POOL))

        reports = prepare_results(results)

        for report in reports:
            update_run_result_with_report(report)


FINISH_TIME = datetime.now()
print("end running terminals {} ...".format(datetime.strftime(FINISH_TIME, "%b %d %y %H:%M:%S %Z")))

ELAPSED = FINISH_TIME - START_TIME
print("elapsed {}...".format(ELAPSED))

input("press Enter to exit ...")
