#!/usr/bin/env python

"""
Runner module.
"""

import time

from datetime import datetime, timedelta

from db.configuration_option import get_option_by_id
from db.run import get_by_configuration_id
from db import run_result

from . import reporting

from util import launch
from util.logging import print_now
from util.sets import create_set_file
from util.run_task import exec_commands
from util.result_extractor import prepare_results
from util import terminal

MAX_WAITS_COUNT = 1
COMMAND_TEMPLATE = '"{}\\terminal.exe" "{}"'

class Metatrader4(object):
    def __init__(self, configuration_id, terminal_pool, verbose = False):
        self.configuration_id = configuration_id
        self.terminal_pool = terminal_pool
        self.verbose = verbose

    def _adjust_reports(self, date_from, reports):
        return reports

    def _create_ini_file(self, data_path, run_result_id, date_from, date_to, symbol, set_file_name):
        ini_file = launch.create_ini_file(data_path, run_result_id, date_from, date_to, symbol, set_file_name)

        return ini_file

    def _get_run_result_date_from(self, run_date_from, run_result_id):
        return run_date_from

    def run(self):
        start_run_time = datetime.now()

        if self.verbose:
            print_now("Start running terminals, configuration_id = {}".format(self.configuration_id))

        reporter = reporting.TradesDiffReporter(self.configuration_id)
        reporter.collect_data()

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
                    run_result_item = run_result.get_for_processing_by_run_id(run_id)

                    # no configuration for processing
                    if run_result_item is None and len(commands) == 0:
                        if self.verbose:
                            print_now("No configuration found for processing, run_name = {}".format(run_name))
                        time.sleep(0.1) # wait for a while
                        number_of_waits = number_of_waits + 1
                        if number_of_waits >= MAX_WAITS_COUNT:
                            break
                        else:
                            continue
                    elif run_result_item is None:
                        break

                    config = get_option_by_id(run_result_item['OptionId'])
                    run_result_id = run_result_item['ResultId']

                    terminal_idx = idx % len(self.terminal_pool)
                    terminal  = self.terminal_pool[terminal_idx]
                    terminal_path = terminal['exe_path']
                    data_path = terminal['data_path']
                    set_file_name = create_set_file(data_path, config, run_result_id)
                    run_result_date_from = self._get_run_result_date_from(date_from, run_result_id)
                    ini_file = self._create_ini_file(data_path, run_result_id, run_result_date_from, date_to, symbol, set_file_name)
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

                reports = self._adjust_reports(date_from, reports)

                for report in reports:
                    run_result.update_run_result_with_report(report)
        
        end_run_time = datetime.now()

        if self.verbose:
            elapsed = end_run_time - start_run_time
            print_now("Running terminals took {}, configuration_id = {}".format(elapsed, self.configuration_id))

        report = reporter.prepare_report()

        return (start_run_time, end_run_time, report)

class SmartMetatrader4(Metatrader4):
    def __init__(self, configuration_id, terminal_pool, verbose = False):
        Metatrader4.__init__(self, configuration_id, terminal_pool, verbose = verbose)
        self.trades_before_run = None

    def _adjust_reports(self, date_from, reports):
        for report in reports:
            date_from = terminal.get_run_result_date_from(date_from, report['ResultId'], self.trades_before_run)

            report['Trades'] = [trade for trade in report['Trades'] if trade['CloseTime'] > date_from]

        return reports

    def _get_run_result_date_from(self, run_date_from, run_result_id):
        date_from = terminal.get_run_result_date_from_formatted(run_date_from, run_result_id, self.trades_before_run)

        return date_from

    def run(self):
        self.trades_before_run = run_result.get_run_result_trades_summary_by_configuration_id(self.configuration_id)

        report = super(SmartMetatrader4, self).run()

        return report
