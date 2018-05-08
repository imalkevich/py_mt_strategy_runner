""" main.py """

__version__ = '0.3'

import argparse
import glob
import os
import time

from db import run
from db import run_result

from util.logging import print_now
from util.start_terminal import init_terminal
from util import terminal

from machine_learning.analytics import TradeResultPredictor

from terminal.runner import SmartMetatrader4

def reset_runner(configuration_id):
    run_result.remove_run_result_trades_by_configuration_id(configuration_id)
    run_result.reset_run_results_by_configuration_id(configuration_id)

    files = glob.glob('/saved_models/*')
    for f in files:
        os.remove(f)

    print_now('Reset before running done, configuration_id = {}'.format(configuration_id))

def smart_refresh_trades(configuration_id):
    runs = run.get_by_configuration_id(configuration_id)
    trades_before_run = run_result.get_run_result_trades_summary_by_configuration_id(configuration_id)

    for run_entry in runs:
        run_id = run_entry['RunId']
        date_from = run_entry['TestDateFrom']

        if trades_before_run.shape[0] > 0:
            trades = trades_before_run[trades_before_run['RunId'] == run_id]

            for _, trades_entry in trades.iterrows():
                result_id = trades_entry['ResultId']
                cutoff_trade_date = terminal.get_run_result_date_from(date_from, result_id, trades_before_run)

                run_result.delete_trades_by_rusult_id_and_close_time(result_id, cutoff_trade_date)
    
    # reset previously collected results, re-think once an issue
    run_result.reset_run_results_by_configuration_id(configuration_id)

    return trades_before_run

def process(configuration_id, refresh, monitor_interval):
    if refresh == True:
        reset_runner(configuration_id)

    for t in terminal.TERMINAL_POOL:
        init_terminal(t['data_path'])

    mt4 = SmartMetatrader4(configuration_id, terminal.TERMINAL_POOL, verbose=True)
    predictor = TradeResultPredictor(configuration_id)

    def do():
        trades_before_run = smart_refresh_trades(configuration_id)
        (_, _, report) = mt4.run(trades_before_run)

        if report['hasNewTrades'] == True:
            print_now('Running TradeResultPredictor, configuration_id = {}'.format(configuration_id))
            predictor.run()
        else:
            print_now('No new trades, configuration_id = {}'.format(configuration_id))

    do()

    if monitor_interval > 0:
        while True:
            time.sleep(int(monitor_interval * 60))
            do()

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
        refresh = bool(int(args['refresh']))

    if args['monitor']:
        monitor = float(args['monitor'])

    configuration_id = int(args['configuration_id'])
    
    print_now('Start running tool for configuration_id = {}, refresh = {}, monitor = {}'.format(configuration_id, refresh, monitor))
    process(configuration_id, refresh, monitor)

def get_parser():
    parser = argparse.ArgumentParser(description='Collect MT4 reports for configurations, monitor new trades, and predict future trades based on history')

    parser.add_argument('-cid', '--configuration_id', help='configuration id', type=str)

    parser.add_argument('-r', '--refresh', 
        help='refresh configuration option results (effectively it means - delete all run results and collect data again)',
        type=int)

    parser.add_argument('-m', '--monitor', 
        help='monitor the configurations interval in minutes - once this parameter is provided, the tool with be running until stopped running configurations and reporting the results', 
        type=str)

    parser.add_argument('-v', '--version', help='displays the current version of analytics module',
                        action='store_true')

    return parser

if __name__ == '__main__':
    command_line_runner()
