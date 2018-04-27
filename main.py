""" main.py """

__version__ = '0.3'

import argparse
import glob
import os
import time

from db.run_result import remove_run_result_trades_by_configuration_id, reset_run_results_by_configuration_id

from util.logging import print_now
from util.start_terminal import init_terminal
from util.terminal import TERMINAL_POOL

from machine_learning.analytics import TradeResultPredictor

from terminal.runner import Metatrader4

def reset_runner(configuration_id):
    remove_run_result_trades_by_configuration_id(configuration_id)
    reset_run_results_by_configuration_id(configuration_id)

    files = glob.glob('/saved_models/*')
    for f in files:
        os.remove(f)

    print_now('Reset before running done, configuration_id = {}'.format(configuration_id))

def run(configuration_id, refresh, monitor_interval):
    if refresh == True:
        reset_runner(configuration_id)

    for terminal in TERMINAL_POOL:
        init_terminal(terminal['data_path'])

    terminal = Metatrader4(configuration_id, TERMINAL_POOL, verbose=True)
    terminal.run()

    predictor = TradeResultPredictor(configuration_id)

    def run_predictor():
        print_now('Running TradeResultPredictor, configuration_id = {}'.format(configuration_id))
        predictor.run()

    run_predictor()

    if monitor_interval > 0:
        while True:
            time.sleep(int(monitor_interval * 60))
            run_predictor()

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['configuration_id']:
        parser.print_help()
        return

    refresh = False
    monitor = -1

    if args['refresh']:
        refresh = bool(args['refresh'])

    if args['monitor']:
        monitor = float(args['monitor'])

    configuration_id = int(args['configuration_id'])
    
    print_now('Start running tool for configuration_id = {}, refresh = {}, monitor = {}'.format(configuration_id, refresh, monitor))
    run(configuration_id, refresh, monitor)

def get_parser():
    parser = argparse.ArgumentParser(description='Collect MT4 reports for configurations, monitor new trades, and predict future trades based on history')

    parser.add_argument('-cid', '--configuration_id', help='configuration id', type=str)

    parser.add_argument('-r', '--refresh', 
        help='refresh configuration option results (effectively it means - delete all run results and collect data again)',
        type=bool)

    parser.add_argument('-m', '--monitor', 
        help='monitor the configurations interval in minutes - once this parameter is provided, the tool with be running until stopped running configurations and reporting the results', 
        type=str)

    parser.add_argument('-v', '--version', help='displays the current version of analytics module',
                        action='store_true')

    return parser

if __name__ == '__main__':
    command_line_runner()
