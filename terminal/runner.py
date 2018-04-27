#!/usr/bin/env python

"""
Runner module.
"""

import time

from datetime import datetime

from db.configuration_option import get_option_by_id
from db.run import get_by_configuration_id
from db.run_result import get_for_processing_by_run_id, update_run_result_with_report

from util.launch import create_ini_file
from util.logging import print_now
from util.sets import create_set_file
from util.run_task import exec_commands
from util.result_extractor import prepare_results

MAX_WAITS_COUNT = 1
COMMAND_TEMPLATE = '"{}\\terminal.exe" "{}"'

class Metatrader4(object):
    def __init__(self, configuration_id, terminal_pool, verbose = False):
        self.configuration_id = configuration_id
        self.terminal_pool = terminal_pool
        self.verbose = verbose

    def run(self):
        start_run_time = datetime.now()

        if self.verbose:
            print_now("Start running terminals, configuration_id = {}".format(self.configuration_id))

        runs = get_by_configuration_id(self.configuration_id)

        for run in runs:
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

                for idx in range(len(self.terminal_pool)):
                    run_result = get_for_processing_by_run_id(run_id)

                    # no configuration for processing
                    if run_result is None and len(commands) == 0:
                        if self.verbose:
                            print_now("No configuration found for processing, run_name = {}".format(run_name))
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

                    terminal_idx = idx % len(self.terminal_pool)
                    terminal  = self.terminal_pool[terminal_idx]
                    terminal_path = terminal['exe_path']
                    data_path = terminal['data_path']
                    set_file_name = create_set_file(data_path, config, run_result_id)
                    ini_file = create_ini_file(data_path, run_result_id, date_from, date_to, symbol, set_file_name)
                    cmd = COMMAND_TEMPLATE.format(terminal_path, ini_file)
                    commands.append(cmd)

                    # for result processing
                    results[data_path] = run_result_id

                if number_of_waits >= MAX_WAITS_COUNT:
                    if self.verbose:
                        print_now("Stop waiting for configuration options to process, configuration_id = {}".format(self.configuration_id))
                    break

                exec_commands(commands, len(self.terminal_pool))

                reports = prepare_results(results)

                for report in reports:
                    update_run_result_with_report(report)
        
        end_run_time = datetime.now()

        if self.verbose:
            elapsed = end_run_time - start_run_time
            print_now("Running terminals took {}, configuration_id = {}".format(elapsed, self.configuration_id))

        return (start_run_time, end_run_time)