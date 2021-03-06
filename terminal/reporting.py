#!/usr/bin/env python

"""
Terminal reporting module.
"""

import pandas as pd

from db import run_result

class TradesDiffReporter(object):
    def __init__(self, configuration_id, trades_before_run):
        self.configuration_id = configuration_id
        self.trades_before_run = trades_before_run
        self.trades_after_run = None

    def _get_new_column_names(self, prefix, columns):
        new_cols_dict = {}
        for col in columns:
            if col == 'ResultId':
                new_cols_dict[col] = col
            else:
                new_cols_dict[col] = '{}_{}'.format(prefix, col)

        return new_cols_dict

    def _generate_report(self, before, after):
        hasNewTrades = False

        if before.shape[0] > 0 and after.shape[0] > 0:
            result = pd.merge(before, after, how='inner', on='ResultId')
            result['TradeDiff'] = result.apply(lambda row: row['after_NumTrades'] - row['before_NumTrades'], axis=1)
            result['HasNewTrades'] = result.apply(lambda row: row['TradeDiff'] > 0 or row['before_MaxCloseTime'] != row['after_MaxCloseTime'], axis=1)

            hasNewTrades = result[result['HasNewTrades'] == True].shape[0] > 0
        elif before.shape[0] == 0 and after.shape[0] > 0:
            hasNewTrades = True

        report = {
            'hasNewTrades': hasNewTrades
        }

        return report
        

    def prepare_report(self):
        columns = self._get_new_column_names('before', self.trades_before_run.columns)
        self.trades_before_run.rename(columns=columns, inplace=True)

        self.trades_after_run = run_result.get_run_result_trades_summary_by_configuration_id(self.configuration_id)
        columns = self._get_new_column_names('after', self.trades_after_run.columns)
        self.trades_after_run.rename(columns=columns, inplace=True)

        report = self._generate_report(self.trades_before_run, self.trades_after_run)

        return report


