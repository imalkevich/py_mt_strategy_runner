#!/usr/bin/env python

"""
Analytics module to predict configuration performance
and send notifications.
"""
import argparse
import numpy as np
import smtplib

from datetime import datetime, timedelta
from email.message import EmailMessage
from prettytable import PrettyTable
from util.config import config
from util.logging import print_now

from . import __version__
from .multilayer_perceptron import MultilayerPerceptron

from db.configuration_option import get_option_by_id
from db.run_result import get_completed_run_results_by_configuration_id
from db.run_result import get_run_result_trades_by_result_id

class TradeResultPredictor(object):
    def __init__(self, configuration_id, verbose=0):
        self.configuration_id = configuration_id
        self.verbose = verbose
        self.start_time = datetime.now()

    def run(self):
        print_now('TradeResultPredictor starting running, configuration = {}'.format(self.configuration_id))

        run_results = get_completed_run_results_by_configuration_id(self.configuration_id)
        tbl = PrettyTable()
        tbl.field_names = [
            'iMA_Period', 
            'TotalNetProfit', 
            'MaximalDrawdown',
            'TotalTrades',
            'Last 3 trades',
            'Last trade date',
            'Predicted 3 trades',
            'Total for predicted 3 trades',
            'Train RMSE / Test RMSE'
        ]

        for run_results in run_results:
            configuration_option = get_option_by_id(run_results['OptionId'])

            trades = get_run_result_trades_by_result_id(run_results['ResultId'])
            # drop unneeded columns
            dataset = trades.drop(trades.columns.difference(['Profit']), 1).values[:,:]

            perceptron = MultilayerPerceptron(run_results['ResultId'], dataset, verbose=self.verbose)
            stats = perceptron.train()
            predicted_trades = perceptron.predict(look_forth = 3)

            testScoreRMSE = 'N/A'
            if stats['TestScore']['RMSE'] != 'N/A':
                testScoreRMSE = '{0:.2f}'.format(stats['TestScore']['RMSE'])

            tbl.add_row([
                configuration_option['iMA_Period'],
                run_results['TotalNetProfit'],
                run_results['MaximalDrawdown'],
                run_results['TotalTrades'],
                ' | '.join(['{0:.2f}'.format(t['Profit']) for idx, t in trades.tail(3).iterrows()]),
                trades['CloseTime'].iloc[-1].strftime('%Y.%m.%d %H:%M'),
                ' | '.join(['{0:.2f}'.format(t) for t in predicted_trades]),
                '{0:.2f}'.format(np.sum(predicted_trades)),
                '{0:.2f} / {1}'.format(stats['TrainScore']['RMSE'], testScoreRMSE)
            ])

        if config.has_section("smtp"):
            smtp_user = config.get('smtp', 'user')
            smtp_password = config.get('smtp', 'password')
            recipients = config.get('smtp', 'recipients')

            tbl_attr = { 
                'style': 'border: 1px solid black; border-collapse: collapse;',
                'cellpadding': 5,
                'border': 1
            }

            subject = 'WSRT predictions {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M'))

            elapsed = datetime.now() - self.start_time
            body = 'Report generated on {}<br/>'.format(datetime.now().strftime('%Y-%m-%d %H:%M'))
            body += 'Report generation took {}<br/>'.format(elapsed)
            
            body += '<br/>'
            body += tbl.get_html_string(attributes=tbl_attr)
            body += '<br/><br/>'

            body += 'Thanks'

            self._send_notification(subject, body, smtp_user, smtp_password, recipients)
            
            print_now('TradeResultPredictor notifications sent, configuration_id = {}'.format(self.configuration_id))

    def _send_notification(self, subject, body, smtp_user, smtp_password, recipients, cc=None, bcc=None):
        msg = EmailMessage()

        msg['Subject'] = subject
        msg.set_content(body)
        msg['From'] = 'analytics@py_mt_strategy_runner.com'
        msg['To'] = recipients
        msg.replace_header('Content-type', 'text/html')
        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()

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