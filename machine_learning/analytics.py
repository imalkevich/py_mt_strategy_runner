#!/usr/bin/env python

"""
Analytics module to predict configuration performance
and send notifications.
"""
import argparse

from . import __version__
from .multilayer_perceptron import MultilayerPerceptron

from db.run_result import get_completed_run_results_by_configuration_id
from db.run_result import get_run_result_trades_by_result_id

class TradeResultPredictor(object):
    def __init__(self, configuration_id):
        self.configuration_id = configuration_id

    def run(self):
        run_results = get_completed_run_results_by_configuration_id(self.configuration_id)
        for run_results in run_results:
            trades = get_run_result_trades_by_result_id(run_results['ResultId'])
            # drop unneeded columns
            trades.drop(trades.columns.difference(['Profit']), 1, inplace=True)
            dataset = trades.values[:,:]

            perceptron = MultilayerPerceptron(dataset)
            stats = perceptron.train()

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['configuration_id']:
        parser.print_help()
        return

    configuration_id = int(args['configuration_id'])

    predictor = TradeResultPredictor(configuration_id)
    predictor.run()

def get_parser():
    parser = argparse.ArgumentParser(description='predict future trades of different configuration options')

    parser.add_argument('-cid', '--configuration_id', help='configuration id', type=str)

    parser.add_argument('-v', '--version', help='displays the current version of analytics module',
                        action='store_true')

    return parser

if __name__ == '__main__':
    command_line_runner()